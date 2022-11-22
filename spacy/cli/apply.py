import tqdm
import srsly

from itertools import chain
from pathlib import Path
from typing import Optional, List, Iterable, cast, Union

from wasabi import msg

from ._util import app, Arg, Opt, setup_gpu, import_code, walk_directory

from ..tokens import Doc, DocBin
from ..vocab import Vocab
from ..util import ensure_path, load_model


path_help = ("Location of the documents to predict on."
             "Can be a single file in .spacy format or "
             ".jsonl file and files with other extensions"
             "are treated as single plain text documents."
             "If a directory is provided "
             "it is traversed recursively to grab all files to "
             "be processed. The files can be a mixture of .spacy"
             ".jsonl and text files. If .jsonl is provided the "
             "specified field is going to be grabbed ('text') "
             "by default.")
out_help = "Path where to save the result .spacy file"
code_help = ("Path to Python file with additional "
             "code (registered functions) to be imported")
gold_help = "Use gold preprocessing provided in the .spacy files"

DocOrStrStream = Union[Iterable[str], Iterable[Doc]]


def _stream_docbin(path: Path, vocab: Vocab) -> Iterable[Doc]:
    """
    Stream Doc objects from DocBin.
    """
    docbin = DocBin().from_disk(path)
    for doc in docbin.get_docs(vocab):
        yield doc


def _stream_jsonl(path: Path, field) -> Iterable[str]:
    """
    Stream "text" field from JSONL. If the field "text" is
    not found it raises error.
    """
    for entry in srsly.read_jsonl(path):
        if field not in entry:
            raise msg.fail(
                f"{path} does not contain the required '{field}' field.",
                exits=1
            )
        else:
            yield entry["text"]


def _stream_texts(paths: Iterable[Path]) -> Iterable[str]:
    """
    Yields strings from text files in paths.
    """
    for path in paths:
        with open(path, 'r') as fin:
            text = fin.read()
            yield text


@app.command("apply")
def apply_cli(
    # fmt: off
    model: str = Arg(..., help="Model name or path"),
    data_path: Path = Arg(..., help=path_help, exists=True),
    output_file: Path = Arg(..., help=out_help, dir_okay=False),
    code_path: Optional[Path] = Opt(None, "--code", "-c", help=code_help),
    field: str = Opt("text", "--field", "-f", help="Field to grab from .jsonl"),
    use_gpu: int = Opt(-1, "--gpu-id", "-g", help="GPU ID or -1 for CPU."),
    batch_size: int = Opt(1, "--batch-size", "-b", help="Batch size."),
    n_process: int = Opt(1, "--n-process", "-n", help="number of processors to use.")
):
    """
    Apply a trained pipeline to documents to get predictions.
    Expects a loadable spaCy pipeline and path to the data, which
    can be a directory or a file.
    The data files can be provided multiple formats: 
        1. .spacy files
        2. .jsonl files with a specified "field" to read the text from.
        3. Files with any other extension are assumed to be containing
           a single document.
    DOCS: https://spacy.io/api/cli#tba
    """
    import_code(code_path)
    setup_gpu(use_gpu)
    apply(data_path, output, model, batch_size, n_process)


def apply(
    data_path: Path,
    output: Path,
    model: str,
    batch_size: int,
    n_process: int,
):
    data_path = ensure_path(data_path)
    output_path = ensure_path(output)
    if not data_path.exists():
        msg.fail("Couldn't find data path.", data_path, exits=1)
    nlp = load_model(model)
    msg.good(f"Loaded model {model}")
    vocab = nlp.vocab
    docbin = DocBin()
    paths = walk_directory(data_path)
    streams: List[DocOrStrStream] = []
    text_files = []
    for path in paths:
        if path.suffix == ".spacy":
            streams.append(_stream_docbin(path, vocab))
        elif path.suffix == ".jsonl":
            streams.append(_stream_jsonl(path, field))
        else:
            text_files.append(path)
    if len(text_files) > 0:
        streams.append(_stream_texts(text_files))
    datagen = cast(DocOrStrStream, chain(*streams))
    for doc in tqdm.tqdm(nlp.pipe(datagen, batch_size=batch_size, n_process=n_process)):
        docbin.add(doc)
    if not output_file.endswith(".spacy"):
        output_file += ".spacy"
    docbin.to_disk(output_file)