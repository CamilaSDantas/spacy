from typing import Iterator, Sequence, Iterable, Optional, Dict, Callable, List, Tuple
from thinc.api import Model, set_dropout_rate, Optimizer, Config
from thinc.types import Floats2d

from .pipe import Pipe
from ..gold import Example, validate_examples
from ..tokens import Doc
from ..vocab import Vocab
from ..language import Language
from ..errors import Errors
from ..util import minibatch


default_model_config = """
[model]
@architectures = "spacy.HashEmbedCNN.v1"
pretrained_vectors = null
width = 96
depth = 4
embed_size = 2000
window_size = 1
maxout_pieces = 3
subword_features = true
"""
DEFAULT_TOK2VEC_MODEL = Config().from_str(default_model_config)["model"]


@Language.factory(
    "tok2vec",
    default_config={
        "model": DEFAULT_TOK2VEC_MODEL,
        "annotation_setter": {"@annotation_setters": "spacy.tensor_setter.v1"},
    },
)
def make_tok2vec(
    nlp: Language,
    model: Model[List[Doc], List[Floats2d]],
    annotation_setter: Callable[[List[Doc], List[Floats2d]], None],
    name: str,
) -> "Tok2Vec":
    return Tok2Vec(nlp.vocab, model, annotation_setter, name=name)


class Tok2Vec(Pipe):
    """Apply a "token-to-vector" model. A single model can be shared between multiple
    components, e.g. to have one embedding and CNN network shared between a
    parser, tagger and NER.

    In order to use the `Tok2Vec` predictions, subsequent components should use
    the `Tok2VecListener` layer as the tok2vec subnetwork of their model.
    During training, the `Tok2Vec` component will save its prediction and backprop
    callback for each batch, so that the subsequent components can backpropagate
    to the shared weights. This implementation is used because it allows us to
    avoid relying on object identity within the models to achieve the parameter
    sharing.

    The tok2vec outputs are stored by the `annotation_setter` - by default this is
    a function that will save the data in the `doc.tensor` attribute.
    """

    def __init__(
        self,
        vocab: Vocab,
        model: Model[List[Doc], List[Floats2d]],
        annotation_setter: Callable[[List[Doc], List[Floats2d]], None],
        *,
        name: str = "tok2vec",
    ) -> None:
        """Initialize a tok2vec component.

        vocab (Vocab): The shared vocabulary.
        model (thinc.api.Model[List[Doc], List[Floats2d]]):
            The Thinc Model powering the pipeline component. It should take
            a list of Doc objects as input, and output a list of 2d float arrays.
        annotation_setter (Callable[[List[Doc], List[Floats2d]], None]): A callback
            to set the tok2vec information onto the batch of `Doc` objects.
        name (str): The component instance name.

        DOCS: https://spacy.io/api/tok2vec#init
        """
        self.vocab = vocab
        self.model = model
        self.name = name
        self.listeners = []
        self.cfg = {}
        self.annotation_setter = annotation_setter

    def add_listener(self, listener: "Tok2VecListener") -> None:
        """Add a listener for a downstream component. Usually internals."""
        self.listeners.append(listener)

    def find_listeners(self, model: Model) -> None:
        """Walk over a model, looking for layers that are Tok2vecListener
        subclasses that have an upstream_name that matches this component.
        Listeners can also set their upstream_name attribute to the wildcard
        string '*' to match any `Tok2Vec`.

        You're unlikely to ever need multiple `Tok2Vec` components, so it's
        fine to leave your listeners upstream_name on '*'.
        """
        for node in model.walk():
            if isinstance(node, Tok2VecListener) and node.upstream_name in (
                "*",
                self.name,
            ):
                self.add_listener(node)

    def __call__(self, doc: Doc) -> Doc:
        """Produce context-sensitive embeddings and store the annotations with the
        annotation_setter.

        docs (Doc): The Doc to process.
        RETURNS (Doc): The processed Doc.

        DOCS: https://spacy.io/api/tok2vec#call
        """
        tokvecses = self.predict([doc])
        self.set_annotations([doc], tokvecses)
        return doc

    def pipe(self, stream: Iterator[Doc], *, batch_size: int = 128) -> Iterator[Doc]:
        """Apply the pipe to a stream of documents. This usually happens under
        the hood when the nlp object is called on a text and all components are
        applied to the Doc.

        stream (Iterable[Doc]): A stream of documents.
        batch_size (int): The number of documents to buffer.
        YIELDS (Doc): Processed documents in order.

        DOCS: https://spacy.io/api/tok2vec#pipe
        """
        for docs in minibatch(stream, batch_size):
            docs = list(docs)
            tokvecses = self.predict(docs)
            self.set_annotations(docs, tokvecses)
            yield from docs

    def predict(self, docs: Iterable[Doc]):
        """Apply the pipeline's model to a batch of docs, without modifying them.
        Returns a single tensor for a batch of documents.

        docs (Iterable[Doc]): The documents to predict.
        RETURNS: Vector representations for each token in the documents.

        DOCS: https://spacy.io/api/tok2vec#predict
        """
        tokvecs = self.model.predict(docs)
        batch_id = Tok2VecListener.get_batch_id(docs)
        for listener in self.listeners:
            listener.receive(batch_id, tokvecs, None)
        return tokvecs

    def set_annotations(self, docs: Sequence[Doc], tokvecses) -> None:
        """Modify a batch of documents, using pre-computed scores.

        docs (Iterable[Doc]): The documents to modify.
        tokvecses: The tensors to set, produced by Tok2Vec.predict.

        DOCS: https://spacy.io/api/tok2vec#set_annotations
        """
        self.annotation_setter(docs, tokvecses)

    def update(
        self,
        examples: Iterable[Example],
        *,
        drop: float = 0.0,
        sgd: Optional[Optimizer] = None,
        losses: Optional[Dict[str, float]] = None,
        set_annotations: bool = False,
    ):
        """Learn from a batch of documents and gold-standard information,
        updating the pipe's model.

        examples (Iterable[Example]): A batch of Example objects.
        drop (float): The dropout rate.
        set_annotations (bool): Whether or not to update the Example objects
            with the predictions.
        sgd (thinc.api.Optimizer): The optimizer.
        losses (Dict[str, float]): Optional record of the loss during training.
            Updated using the component name as the key.
        RETURNS (Dict[str, float]): The updated losses dictionary.

        DOCS: https://spacy.io/api/tok2vec#update
        """
        if losses is None:
            losses = {}
        validate_examples(examples, "Tok2Vec.update")
        docs = [eg.predicted for eg in examples]
        set_dropout_rate(self.model, drop)
        tokvecs, bp_tokvecs = self.model.begin_update(docs)
        d_tokvecs = [self.model.ops.alloc2f(*t2v.shape) for t2v in tokvecs]
        losses.setdefault(self.name, 0.0)

        def accumulate_gradient(one_d_tokvecs):
            """Accumulate tok2vec loss and gradient. This is passed as a callback
            to all but the last listener. Only the last one does the backprop.
            """
            nonlocal d_tokvecs
            for i in range(len(one_d_tokvecs)):
                d_tokvecs[i] += one_d_tokvecs[i]
                losses[self.name] += float((one_d_tokvecs[i] ** 2).sum())

        def backprop(one_d_tokvecs):
            """Callback to actually do the backprop. Passed to last listener."""
            accumulate_gradient(one_d_tokvecs)
            d_docs = bp_tokvecs(d_tokvecs)
            if sgd is not None:
                self.model.finish_update(sgd)
            return d_docs

        batch_id = Tok2VecListener.get_batch_id(docs)
        for listener in self.listeners[:-1]:
            listener.receive(batch_id, tokvecs, accumulate_gradient)
        if self.listeners:
            self.listeners[-1].receive(batch_id, tokvecs, backprop)
        if set_annotations:
            self.set_annotations(docs, tokvecs)
        return losses

    def get_loss(self, examples, scores) -> None:
        pass

    def begin_training(
        self,
        get_examples: Callable[[], Iterable[Example]],
        *,
        pipeline: Optional[List[Tuple[str, Callable[[Doc], Doc]]]] = None,
        sgd: Optional[Optimizer] = None,
    ):
        """Initialize the pipe for training, using data examples if available.

        get_examples (Callable[[], Iterable[Example]]): Optional function that
            returns gold-standard Example objects.
        pipeline (List[Tuple[str, Callable]]): Optional list of pipeline
            components that this component is part of. Corresponds to
            nlp.pipeline.
        sgd (thinc.api.Optimizer): Optional optimizer. Will be created with
            create_optimizer if it doesn't exist.
        RETURNS (thinc.api.Optimizer): The optimizer.

        DOCS: https://spacy.io/api/tok2vec#begin_training
        """
        docs = [Doc(self.vocab, words=["hello"])]
        self.model.initialize(X=docs)

    def add_label(self, label):
        raise NotImplementedError


class Tok2VecListener(Model):
    """A layer that gets fed its answers from an upstream connection,
    for instance from a component earlier in the pipeline.

    The Tok2VecListener layer is used as a sublayer within a component such
    as a parser, NER or text categorizer. Usually you'll have multiple listeners
    connecting to a single upstream Tok2Vec component, that's earlier in the
    pipeline. The Tok2VecListener layers act as proxies, passing the predictions
    from the Tok2Vec component into downstream components, and communicating
    gradients back upstream.
    """

    name = "tok2vec-listener"

    def __init__(self, upstream_name: str, width: int) -> None:
        """
        upstream_name (str): A string to identify the 'upstream' Tok2Vec component
            to communicate with. The upstream name should either be the wildcard
            string '*', or the name of the `Tok2Vec` component. You'll almost
            never have multiple upstream Tok2Vec components, so the wildcard
            string will almost always be fine.
        width (int):
            The width of the vectors produced by the upstream tok2vec component.
        """
        Model.__init__(self, name=self.name, forward=forward, dims={"nO": width})
        self.upstream_name = upstream_name
        self._batch_id = None
        self._outputs = None
        self._backprop = None

    @classmethod
    def get_batch_id(cls, inputs: List[Doc]) -> int:
        """Calculate a content-sensitive hash of the batch of documents, to check
        whether the next batch of documents is unexpected.
        """
        return sum(sum(token.orth for token in doc) for doc in inputs)

    def receive(self, batch_id: int, outputs, backprop) -> None:
        """Store a batch of training predictions and a backprop callback. The
        predictions and callback are produced by the upstream Tok2Vec component,
        and later will be used when the listener's component's model is called.
        """
        self._batch_id = batch_id
        self._outputs = outputs
        self._backprop = backprop

    def verify_inputs(self, inputs) -> bool:
        """Check that the batch of Doc objects matches the ones we have a
        prediction for.
        """
        if self._batch_id is None and self._outputs is None:
            raise ValueError(Errors.E954)
        else:
            batch_id = self.get_batch_id(inputs)
            if batch_id != self._batch_id:
                raise ValueError(Errors.E953.format(id1=batch_id, id2=self._batch_id))
            else:
                return True


def forward(model: Tok2VecListener, inputs, is_train: bool):
    """Supply the outputs from the upstream Tok2Vec component."""
    bp = model._backprop
    if not is_train:
        bp = lambda dX: []
    model.verify_inputs(inputs)
    return model._outputs, bp
