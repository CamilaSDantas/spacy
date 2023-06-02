from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

from thinc.api import Config, Model, Optimizer, set_dropout_rate
from thinc.types import Floats2d

from spacy.language import Language
from spacy.pipeline.trainable_pipe import TrainablePipe
from spacy.scorer import Scorer
from spacy.tokens import Doc, Span
from spacy.training import Example
from spacy.errors import Errors

from ..util import registry
from .spancat import DEFAULT_SPANS_KEY

span_finder_default_config = """
[model]
@architectures = "spacy.SpanFinder.v1"

[model.scorer]
@layers = "spacy.LinearLogistic.v1"
nO = 2

[model.tok2vec]
@architectures = "spacy.Tok2Vec.v2"

[model.tok2vec.embed]
@architectures = "spacy.MultiHashEmbed.v2"
width = 96
rows = [5000, 1000, 2500, 1000]
attrs = ["NORM", "PREFIX", "SUFFIX", "SHAPE"]
include_static_vectors = false

[model.tok2vec.encode]
@architectures = "spacy.MaxoutWindowEncoder.v2"
width = ${model.tok2vec.embed.width}
window_size = 1
maxout_pieces = 3
depth = 4
"""

DEFAULT_SPAN_FINDER_MODEL = Config().from_str(span_finder_default_config)["model"]


@Language.factory(
    "span_finder",
    assigns=["doc.spans"],
    default_config={
        "threshold": 0.5,
        "model": DEFAULT_SPAN_FINDER_MODEL,
        "spans_key": DEFAULT_SPANS_KEY,
        "max_length": None,
        "min_length": None,
        "scorer": {"@scorers": "spacy.span_finder_scorer.v1"},
    },
    default_score_weights={
        f"span_finder_{DEFAULT_SPANS_KEY}_f": 1.0,
        f"span_finder_{DEFAULT_SPANS_KEY}_p": 0.0,
        f"span_finder_{DEFAULT_SPANS_KEY}_r": 0.0,
    },
)
def make_span_finder(
    nlp: Language,
    name: str,
    model: Model[Iterable[Doc], Floats2d],
    spans_key: str,
    threshold: float,
    max_length: Optional[int],
    min_length: Optional[int],
    scorer: Optional[Callable],
) -> "SpanFinder":
    """Create a SpanFinder component. The component predicts whether a token is
    the start or the end of a potential span.

    model (Model[List[Doc], Floats2d]): A model instance that
        is given a list of documents and predicts a probability for each token.
    spans_key (str): Key of the doc.spans dict to save the spans under. During
        initialization and training, the component will look for spans on the
        reference document under the same key.
    threshold (float): Minimum probability to consider a prediction positive.
    max_length (Optional[int]): Max length of the produced spans, defaults to None meaning unlimited length.
    min_length (Optional[int]): Min length of the produced spans, defaults to None meaining shortest span is length 1.
    scorer (Optional[Callable]): The scoring method. Defaults to
        Scorer.score_spans for the Doc.spans[spans_key] with overlapping
        spans allowed.
    """
    return SpanFinder(
        nlp,
        model=model,
        threshold=threshold,
        name=name,
        scorer=scorer,
        max_length=max_length,
        min_length=min_length,
        spans_key=spans_key,
    )


@registry.scorers("spacy.span_finder_scorer.v1")
def make_span_finder_scorer():
    return span_finder_score


def span_finder_score(examples: Iterable[Example], **kwargs) -> Dict[str, Any]:
    kwargs = dict(kwargs)
    attr_prefix = "span_finder_"
    key = kwargs["spans_key"]
    kwargs.setdefault("attr", f"{attr_prefix}{key}")
    kwargs.setdefault(
        "getter", lambda doc, key: doc.spans.get(key[len(attr_prefix) :], [])
    )
    kwargs.setdefault("has_annotation", lambda doc: key in doc.spans)
    kwargs.setdefault("allow_overlap", True)
    kwargs.setdefault("labeled", False)
    scores = Scorer.score_spans(examples, **kwargs)
    scores.pop(f"{kwargs['attr']}_per_type", None)
    return scores


class _MaxInt(int):
    def __le__(self, other):
        return False

    def __lt__(self, other):
        return False

    def __ge__(self, other):
        return True

    def __gt__(self, other):
        return True


def _char_indices(span: Span) -> Tuple[int, int]:
    start = span[0].idx
    end = span[-1].idx + len(span[-1])
    return start, end


class SpanFinder(TrainablePipe):
    """Pipeline that learns span boundaries"""

    def __init__(
        self,
        nlp: Language,
        model: Model[Iterable[Doc], Floats2d],
        name: str = "span_finder",
        *,
        spans_key: str = DEFAULT_SPANS_KEY,
        threshold: float = 0.5,
        max_length: Optional[int] = None,
        min_length: Optional[int] = None,
        scorer: Optional[Callable] = span_finder_score,
    ) -> None:
        """Initialize the span boundary detector.
        model (thinc.api.Model): The Thinc Model powering the pipeline component.
        name (str): The component instance name, used to add entries to the
            losses during training.
        threshold (float): Minimum probability to consider a prediction
            positive.
        scorer (Optional[Callable]): The scoring method.
        spans_key (str): Key of the doc.spans dict to save the spans under. During
            initialization and training, the component will look for spans on the
            reference document under the same key.
        max_length (Optional[int]): Max length of the produced spans, defaults to None meaning unlimited length.
        min_length (Optional[int]): Min length of the produced spans, defaults to None meaining shortest span is length 1.
        """
        self.vocab = nlp.vocab
        self.threshold = threshold
        if max_length is None:
            max_length = _MaxInt()
        if min_length is None:
            min_length = 1
        if max_length < 1 or min_length < 1:
            raise ValueError(
                Errors.E1052.format(min_length=min_length, max_length=max_length)
            )
        self.min_length = min_length
        self.max_length = max_length
        self.spans_key = spans_key
        self.model = model
        self.name = name
        self.scorer = scorer
        self.cfg = {"spans_key": spans_key}

    def predict(self, docs: Iterable[Doc]):
        """Apply the pipeline's model to a batch of docs, without modifying them.
        docs (Iterable[Doc]): The documents to predict.
        RETURNS: The models prediction for each document.
        """
        scores = self.model.predict(docs)
        return scores

    def set_annotations(self, docs: Iterable[Doc], scores: Floats2d) -> None:
        """Modify a batch of Doc objects, using pre-computed scores.
        docs (Iterable[Doc]): The documents to modify.
        scores: The scores to set, produced by SpanFinder predict method.
        """
        offset = 0
        for i, doc in enumerate(docs):
            doc.spans[self.spans_key] = []
            starts = []
            ends = []
            doc_scores = scores[offset : offset + len(doc)]

            for token, token_score in zip(doc, doc_scores):
                if token_score[0] >= self.threshold:
                    starts.append(token.i)
                if token_score[1] >= self.threshold:
                    ends.append(token.i)

            for start in starts:
                for end in ends:
                    span_length = end + 1 - start
                    if span_length > self.max_length:
                        break
                    elif self.min_length <= span_length:
                        doc.spans[self.spans_key].append(doc[start : end + 1])
            offset += len(doc)

    def update(
        self,
        examples: Iterable[Example],
        *,
        drop: float = 0.0,
        sgd: Optional[Optimizer] = None,
        losses: Optional[Dict[str, float]] = None,
    ) -> Dict[str, float]:
        """Learn from a batch of documents and gold-standard information,
        updating the pipe's model. Delegates to predict and get_loss.
        examples (Iterable[Example]): A batch of Example objects.
        drop (float): The dropout rate.
        sgd (Optional[thinc.api.Optimizer]): The optimizer.
        losses (Optional[Dict[str, float]]): Optional record of the loss during training.
            Updated using the component name as the key.
        RETURNS (Dict[str, float]): The updated losses dictionary.
        """
        if losses is None:
            losses = {}
        losses.setdefault(self.name, 0.0)
        predicted = [eg.predicted for eg in examples]
        set_dropout_rate(self.model, drop)
        scores, backprop_scores = self.model.begin_update(predicted)
        loss, d_scores = self.get_loss(examples, scores)
        backprop_scores(d_scores)
        if sgd is not None:
            self.finish_update(sgd)
        losses[self.name] += loss
        return losses

    def get_loss(self, examples, scores) -> Tuple[float, Floats2d]:
        """Find the loss and gradient of loss for the batch of documents and
        their predicted scores.
        examples (Iterable[Examples]): The batch of examples.
        scores: Scores representing the model's predictions.
        RETURNS (Tuple[float, float]): The loss and the gradient.
        """
        truths, masks = self._get_aligned_truth_scores(examples, self.model.ops)
        d_scores = scores - self.model.ops.asarray2f(truths)
        d_scores *= masks
        loss = float((d_scores**2).sum())
        return loss, d_scores

    def _get_aligned_truth_scores(self, examples, ops) -> Tuple[Floats2d, Floats2d]:
        """Align scores of the predictions to the references for calculating the loss"""
        truths = []
        masks = []
        for eg in examples:
            if eg.x.text != eg.y.text:
                raise ValueError(Errors.E1053.format(component="span_finder"))
            n_tokens = len(eg.predicted)
            truth = ops.xp.zeros((n_tokens, 2), dtype="float32")
            mask = ops.xp.ones((n_tokens, 2), dtype="float32")
            if self.spans_key in eg.reference.spans:
                for span in eg.reference.spans[self.spans_key]:
                    ref_start_char, ref_end_char = _char_indices(span)
                    pred_span = eg.predicted.char_span(
                        ref_start_char, ref_end_char, alignment_mode="expand"
                    )
                    pred_start_char, pred_end_char = _char_indices(pred_span)
                    start_match = pred_start_char == ref_start_char
                    end_match = pred_end_char == ref_end_char
                    if start_match:
                        truth[pred_span[0].i, 0] = 1
                    else:
                        mask[pred_span[0].i, 0] = 0
                    if end_match:
                        truth[pred_span[-1].i, 1] = 1
                    else:
                        mask[pred_span[-1].i, 1] = 0
            truths.append(truth)
            masks.append(mask)
        truths = ops.xp.concatenate(truths, axis=0)
        masks = ops.xp.concatenate(masks, axis=0)
        return truths, masks

    def initialize(
        self,
        get_examples: Callable[[], Iterable[Example]],
        *,
        nlp: Optional[Language] = None,
    ) -> None:
        """Initialize the pipe for training, using a representative set
        of data examples.
        get_examples (Callable[[], Iterable[Example]]): Function that
            returns a representative sample of gold-standard Example objects.
        nlp (Optional[Language]): The current nlp object the component is part of.
        """
        subbatch: List[Example] = []

        for eg in get_examples():
            if len(subbatch) < 10:
                subbatch.append(eg)

        if subbatch:
            docs = [eg.reference for eg in subbatch]
            Y, _ = self._get_aligned_truth_scores(subbatch, self.model.ops)
            self.model.initialize(X=docs, Y=Y)
        else:
            self.model.initialize()
