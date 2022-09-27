# cython: infer_types=True, cdivision=True, boundscheck=False, binding=True
from __future__ import print_function
from typing import List
from cymem.cymem cimport Pool
cimport numpy as np
from itertools import islice
from libcpp.vector cimport vector
from libc.string cimport memset, memcpy
from libc.stdlib cimport calloc, free
import random
import contextlib

import srsly
from thinc.api import get_ops, set_dropout_rate, CupyOps, NumpyOps
from thinc.api import get_array_module
from thinc.extra.search cimport Beam
from thinc.types import Ints1d
import numpy.random
import numpy
import warnings

from ._parser_internals.stateclass cimport StateC, StateClass
from ._parser_internals.search cimport Beam
from ..tokens.doc cimport Doc
from .trainable_pipe cimport TrainablePipe
from ._parser_internals cimport _beam_utils
from ._parser_internals import _beam_utils
from ..vocab cimport Vocab
from ._parser_internals.transition_system cimport TransitionSystem
from ..typedefs cimport weight_t

from ..training import validate_examples, validate_get_examples
from ..errors import Errors, Warnings
from .. import util


NUMPY_OPS = NumpyOps()


cdef class Parser(TrainablePipe):
    """
    Base class of the DependencyParser and EntityRecognizer.
    """

    def __init__(
        self,
        Vocab vocab,
        model,
        name="base_parser",
        moves=None,
        *,
        update_with_oracle_cut_size,
        min_action_freq,
        learn_tokens,
        beam_width=1,
        beam_density=0.0,
        beam_update_prob=0.0,
        multitasks=tuple(),
        incorrect_spans_key=None,
        scorer=None,
    ):
        """Create a Parser.

        vocab (Vocab): The vocabulary object. Must be shared with documents
            to be processed. The value is set to the `.vocab` attribute.
        model (Model): The model for the transition-based parser. The model needs
            to have a specific substructure of named components --- see the
            spacy.ml.tb_framework.TransitionModel for details.
        name (str): The name of the pipeline component
        moves (Optional[TransitionSystem]): This defines how the parse-state is created,
            updated and evaluated. If 'moves' is None, a new instance is
            created with `self.TransitionSystem()`. Defaults to `None`.
        update_with_oracle_cut_size (int): During training, cut long sequences into
            shorter segments by creating intermediate states based on the gold-standard
            history. The model is not very sensitive to this parameter, so you usually
            won't need to change it. 100 is a good default.
        min_action_freq (int): The minimum frequency of labelled actions to retain.
            Rarer labelled actions have their label backed-off to "dep". While this
            primarily affects the label accuracy, it can also affect the attachment
            structure, as the labels are used to represent the pseudo-projectivity
            transformation.
        learn_tokens (bool): Whether to learn to merge subtokens that are split
            relative to the gold standard. Experimental.
        beam_width (int): The number of candidate analyses to maintain.
        beam_density (float): The minimum ratio between the scores of the first and
            last candidates in the beam. This allows the parser to avoid exploring
            candidates that are too far behind. This is mostly intended to improve
            efficiency, but it can also improve accuracy as deeper search is not
            always better.
        beam_update_prob (float): The chance of making a beam update, instead of a
            greedy update. Greedy updates are an approximation for the beam updates,
            and are faster to compute.
        multitasks: additional multi-tasking components. Experimental.
        incorrect_spans_key (Optional[str]): Identifies spans that are known
            to be incorrect entity annotations. The incorrect entity annotations
            can be stored in the span group, under this key.
        scorer (Optional[Callable]): The scoring method. Defaults to None.
        """
        self.vocab = vocab
        self.name = name
        cfg = {
            "moves": moves,
            "update_with_oracle_cut_size": update_with_oracle_cut_size,
            "multitasks": list(multitasks),
            "min_action_freq": min_action_freq,
            "learn_tokens": learn_tokens,
            "beam_width": beam_width,
            "beam_density": beam_density,
            "beam_update_prob": beam_update_prob,
            "incorrect_spans_key": incorrect_spans_key
        }
        if moves is None:
            # EntityRecognizer -> BiluoPushDown
            # DependencyParser -> ArcEager
            moves = self.TransitionSystem(
                self.vocab.strings,
                incorrect_spans_key=incorrect_spans_key
            )
        self.moves = moves
        self.model = model
        if self.moves.n_moves != 0:
            self.set_output(self.moves.n_moves)
        self.cfg = cfg
        self._multitasks = []
        for multitask in cfg["multitasks"]:
            self.add_multitask_objective(multitask)

        self._rehearsal_model = None
        self.scorer = scorer
        self._cpu_ops = get_ops("cpu") if isinstance(self.model.ops, CupyOps) else self.model.ops

    def __getnewargs_ex__(self):
        """This allows pickling the Parser and its keyword-only init arguments"""
        args = (self.vocab, self.model, self.name, self.moves)
        return args, self.cfg

    @property
    def move_names(self):
        names = []
        cdef TransitionSystem moves = self.moves
        for i in range(self.moves.n_moves):
            name = self.moves.move_name(moves.c[i].move, moves.c[i].label)
            # Explicitly removing the internal "U-" token used for blocking entities
            if name != "U-":
                names.append(name)
        return names

    @property
    def labels(self):
        class_names = [self.moves.get_class_name(i) for i in range(self.moves.n_moves)]
        return class_names

    @property
    def label_data(self):
        return self.moves.labels

    @property
    def tok2vec(self):
        """Return the embedding and convolutional layer of the model."""
        return self.model.get_ref("tok2vec")

    @property
    def postprocesses(self):
        # Available for subclasses, e.g. to deprojectivize
        return []

    @property
    def incorrect_spans_key(self):
        return self.cfg["incorrect_spans_key"]

    def add_label(self, label):
        resized = False
        for action in self.moves.action_types:
            added = self.moves.add_action(action, label)
            if added:
                resized = True
        if resized:
            self._resize()
            self.vocab.strings.add(label)
            return 1
        return 0

    def _ensure_labels_are_added(self, docs):
        """Ensure that all labels for a batch of docs are added."""
        resized = False
        labels = set()
        for doc in docs:
            labels.update(self.moves.get_doc_labels(doc))
        for label in labels:
            for action in self.moves.action_types:
                added = self.moves.add_action(action, label)
                if added:
                    self.vocab.strings.add(label)
                    resized = True
        if resized:
            self._resize()
            return 1
        return 0

    def _resize(self):
        self.model.attrs["resize_output"](self.model, self.moves.n_moves)
        if self._rehearsal_model not in (True, False, None):
            self._rehearsal_model.attrs["resize_output"](
                self._rehearsal_model, self.moves.n_moves
            )

    def add_multitask_objective(self, target):
        # Defined in subclasses, to avoid circular import
        raise NotImplementedError

    def init_multitask_objectives(self, get_examples, pipeline, **cfg):
        """Setup models for secondary objectives, to benefit from multi-task
        learning. This method is intended to be overridden by subclasses.

        For instance, the dependency parser can benefit from sharing
        an input representation with a label prediction model. These auxiliary
        models are discarded after training.
        """
        pass

    def use_params(self, params):
        # Can't decorate cdef class :(. Workaround.
        with self.model.use_params(params):
            yield

    def pipe(self, docs, *, int batch_size=256):
        """Process a stream of documents.

        stream: The sequence of documents to process.
        batch_size (int): Number of documents to accumulate into a working set.

        YIELDS (Doc): Documents, in order.
        """
        cdef Doc doc
        error_handler = self.get_error_handler()
        for batch in util.minibatch(docs, size=batch_size):
            batch_in_order = list(batch)
            try:
                by_length = sorted(batch, key=lambda doc: len(doc))
                for subbatch in util.minibatch(by_length, size=max(batch_size//4, 2)):
                    subbatch = list(subbatch)
                    parse_states = self.predict(subbatch)
                    self.set_annotations(subbatch, parse_states)
                yield from batch_in_order
            except Exception as e:
                error_handler(self.name, self, batch_in_order, e)


    def predict(self, docs):
        if isinstance(docs, Doc):
            docs = [docs]
        self._ensure_labels_are_added(docs)
        if not any(len(doc) for doc in docs):
            result = self.moves.init_batch(docs)
            return result
        with _change_attrs(self.model, beam_width=self.cfg["beam_width"], beam_density=self.cfg["beam_density"]):
            states_or_beams, _ = self.model.predict((docs, self.moves))
        return states_or_beams

    def greedy_parse(self, docs, drop=0.):
        self._resize()
        self._ensure_labels_are_added(docs)
        with _change_attrs(self.model, beam_width=1):
            states, _ = self.model.predict((docs, self.moves))
        return states

    def beam_parse(self, docs, int beam_width, float drop=0., beam_density=0.):
        self._ensure_labels_are_added(docs)
        with _change_attrs(self.model, beam_width=self.cfg["beam_width"], beam_density=self.cfg["beam_density"]):
            beams, _ = self.model.predict((docs, self.moves))
        return beams

    def set_annotations(self, docs, states_or_beams):
        cdef StateClass state
        cdef Beam beam
        cdef Doc doc
        states = _beam_utils.collect_states(states_or_beams, docs)
        for i, (state, doc) in enumerate(zip(states, docs)):
            self.moves.set_annotations(state, doc)
            for hook in self.postprocesses:
                hook(doc)

    def update(self, examples, *, drop=0., sgd=None, losses=None):
        cdef StateClass state
        if losses is None:
            losses = {}
        losses.setdefault(self.name, 0.)
        validate_examples(examples, "Parser.update")
        self._ensure_labels_are_added(
            [eg.x for eg in examples] + [eg.y for eg in examples]
        )
        for multitask in self._multitasks:
            multitask.update(examples, drop=drop, sgd=sgd)
        # We need to take care to act on the whole batch, because we might be
        # getting vectors via a listener.
        n_examples = len([eg for eg in examples if self.moves.has_gold(eg)])
        if n_examples == 0:
            return losses
        set_dropout_rate(self.model, drop)
        docs = [eg.x for eg in examples if len(eg.x)]
        (states, scores), backprop_scores = self.model.begin_update((docs, self.moves))
        if sum(s.shape[0] for s in scores) == 0:
            return losses
        d_scores = self.get_loss((states, scores), examples)
        backprop_scores((states, d_scores))
        if sgd not in (None, False):
            self.finish_update(sgd)
        losses[self.name] += float((d_scores**2).sum())
        # Ugh, this is annoying. If we're working on GPU, we want to free the
        # memory ASAP. It seems that Python doesn't necessarily get around to
        # removing these in time if we don't explicitly delete? It's confusing.
        del backprop_scores
        return losses

    def get_loss(self, states_scores, examples):
        states, scores = states_scores
        scores = self.model.ops.xp.vstack(scores)
        costs = self._get_costs_from_histories(
            examples,
            [list(state.history) for state in states]
        )
        xp = get_array_module(scores)
        best_costs = costs.min(axis=1, keepdims=True)
        gscores = scores.copy()
        min_score = scores.min() - 1000
        assert costs.shape == scores.shape, (costs.shape, scores.shape)
        gscores[costs > best_costs] = min_score
        max_ = scores.max(axis=1, keepdims=True)
        gmax = gscores.max(axis=1, keepdims=True)
        exp_scores = xp.exp(scores - max_)
        exp_gscores = xp.exp(gscores - gmax)
        Z = exp_scores.sum(axis=1, keepdims=True)
        gZ = exp_gscores.sum(axis=1, keepdims=True)
        d_scores = exp_scores / Z
        d_scores -= (costs <= best_costs) * (exp_gscores / gZ)
        return d_scores

    def _get_costs_from_histories(self, examples, histories):
        cdef TransitionSystem moves = self.moves
        cdef StateClass state
        cdef int clas
        cdef int nF = self.model.get_dim("nF")
        cdef int nO = moves.n_moves
        cdef int nS = sum([len(history) for history in histories])
        cdef Pool mem = Pool()
        cdef np.ndarray costs_i
        is_valid = <int*>mem.alloc(nO, sizeof(int))
        states = moves.init_batch([eg.x for eg in examples])
        batch = []
        for eg, s, h in zip(examples, states, histories):
            if not s.is_final():
                gold = moves.init_gold(s, eg)
                batch.append((eg, s, h, gold))
        output = []
        while batch:
            costs = numpy.zeros((len(batch), nO), dtype="f")
            for i, (eg, state, history, gold) in enumerate(batch):
                costs_i = costs[i]
                clas = history.pop(0)
                moves.set_costs(is_valid, <weight_t*>costs_i.data, state.c, gold)
                action = moves.c[clas]
                action.do(state.c, action.label)
                state.c.history.push_back(clas)
            output.append(costs)
            batch = [(eg, s, h, g) for eg, s, h, g in batch if len(h) != 0]
        return self.model.ops.xp.vstack(output)

    def rehearse(self, examples, sgd=None, losses=None, **cfg):
        """Perform a "rehearsal" update, to prevent catastrophic forgetting."""
        if losses is None:
            losses = {}
        for multitask in self._multitasks:
            if hasattr(multitask, 'rehearse'):
                multitask.rehearse(examples, losses=losses, sgd=sgd)
        if self._rehearsal_model is None:
            return None
        losses.setdefault(self.name, 0.0)
        validate_examples(examples, "Parser.rehearse")
        docs = [eg.predicted for eg in examples]
        # This is pretty dirty, but the NER can resize itself in init_batch,
        # if labels are missing. We therefore have to check whether we need to
        # expand our model output.
        self._resize()
        # Prepare the stepwise model, and get the callback for finishing the batch
        set_dropout_rate(self._rehearsal_model, 0.0)
        set_dropout_rate(self.model, 0.0)
        (student_states, student_scores), backprop_scores = self.model.begin_update((docs, self.moves))
        actions = states2actions(student_states)
        _, teacher_scores = self._rehearsal_model.predict((docs, self.moves, actions))

        teacher_scores = self.model.ops.xp.vstack(teacher_scores)
        student_scores = self.model.ops.xp.vstack(student_scores)
        assert teacher_scores.shape == student_scores.shape

        d_scores = (student_scores - teacher_scores) / teacher_scores.shape[0]
        # If all weights for an output are 0 in the original model, don't
        # supervise that output. This allows us to add classes.
        loss = (d_scores**2).sum() / d_scores.size
        backprop_scores((student_states, d_scores))

        if sgd is not None:
            self.finish_update(sgd)
        losses[self.name] += loss

        return losses

    def update_beam(self, examples, *, beam_width,
            drop=0., sgd=None, losses=None, beam_density=0.0):
        raise NotImplementedError

    def set_output(self, nO):
        self.model.attrs["resize_output"](self.model, nO)

    def initialize(self, get_examples, nlp=None, labels=None):
        validate_get_examples(get_examples, "Parser.initialize")
        util.check_lexeme_norms(self.vocab, "parser or NER")
        if labels is not None:
            actions = dict(labels)
        else:
            actions = self.moves.get_actions(
                examples=get_examples(),
                min_freq=self.cfg['min_action_freq'],
                learn_tokens=self.cfg["learn_tokens"]
            )
        for action, labels in self.moves.labels.items():
            actions.setdefault(action, {})
            for label, freq in labels.items():
                if label not in actions[action]:
                    actions[action][label] = freq
        self.moves.initialize_actions(actions)
        # make sure we resize so we have an appropriate upper layer
        self._resize()
        doc_sample = []
        if nlp is not None:
            for name, component in nlp.pipeline:
                if component is self:
                    break
                # non-trainable components may have a pipe() implementation that refers to dummy
                # predict and set_annotations methods
                if hasattr(component, "pipe"):
                    doc_sample = list(component.pipe(doc_sample, batch_size=8))
                else:
                    doc_sample = [component(doc) for doc in doc_sample]
        if not doc_sample:
            for example in islice(get_examples(), 10):
                doc_sample.append(example.predicted)
        assert len(doc_sample) > 0, Errors.E923.format(name=self.name)
        self.model.initialize((doc_sample, self.moves))
        if nlp is not None:
            self.init_multitask_objectives(get_examples, nlp.pipeline)

    def to_disk(self, path, exclude=tuple()):
        serializers = {
            "model": lambda p: (self.model.to_disk(p) if self.model is not True else True),
            "vocab": lambda p: self.vocab.to_disk(p, exclude=exclude),
            "moves": lambda p: self.moves.to_disk(p, exclude=["strings"]),
            "cfg": lambda p: srsly.write_json(p, self.cfg)
        }
        util.to_disk(path, serializers, exclude)

    def from_disk(self, path, exclude=tuple()):
        deserializers = {
            "vocab": lambda p: self.vocab.from_disk(p, exclude=exclude),
            "moves": lambda p: self.moves.from_disk(p, exclude=["strings"]),
            "cfg": lambda p: self.cfg.update(srsly.read_json(p)),
            "model": lambda p: None,
        }
        util.from_disk(path, deserializers, exclude)
        if "model" not in exclude:
            path = util.ensure_path(path)
            with (path / "model").open("rb") as file_:
                bytes_data = file_.read()
            try:
                self._resize()
                self.model.from_bytes(bytes_data)
            except AttributeError:
                raise ValueError(Errors.E149)
        return self

    def to_bytes(self, exclude=tuple()):
        serializers = {
            "model": lambda: (self.model.to_bytes()),
            "vocab": lambda: self.vocab.to_bytes(exclude=exclude),
            "moves": lambda: self.moves.to_bytes(exclude=["strings"]),
            "cfg": lambda: srsly.json_dumps(self.cfg, indent=2, sort_keys=True)
        }
        return util.to_bytes(serializers, exclude)

    def from_bytes(self, bytes_data, exclude=tuple()):
        deserializers = {
            "vocab": lambda b: self.vocab.from_bytes(b, exclude=exclude),
            "moves": lambda b: self.moves.from_bytes(b, exclude=["strings"]),
            "cfg": lambda b: self.cfg.update(srsly.json_loads(b)),
            "model": lambda b: None,
        }
        msg = util.from_bytes(bytes_data, deserializers, exclude)
        if 'model' not in exclude:
            if 'model' in msg:
                try:
                    self.model.from_bytes(msg['model'])
                except AttributeError:
                    raise ValueError(Errors.E149) from None
        return self


@contextlib.contextmanager
def _change_attrs(model, **kwargs):
    """Temporarily modify a thinc model's attributes."""
    unset = object()
    old_attrs = {}
    for key, value in kwargs.items():
        old_attrs[key] = model.attrs.get(key, unset)
        model.attrs[key] = value
    yield model
    for key, value in old_attrs.items():
        if value is unset:
            model.attrs.pop(key)
        else:
            model.attrs[key] = value


def states2actions(states: List[StateClass]) -> List[Ints1d]:
    cdef int step
    cdef StateClass state
    cdef StateC* c_state
    actions = []
    while True:
        step = len(actions)

        step_actions = []
        for state in states:
            c_state = state.c
            if step < c_state.history.size():
                step_actions.append(c_state.history[step])

        # We are done if we have exhausted all histories.
        if len(step_actions) == 0:
            break

        actions.append(numpy.array(step_actions, dtype="i"))

    return actions
