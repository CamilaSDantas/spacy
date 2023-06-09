import os
import math
from collections import Counter
from typing import Tuple, List, Dict, Any
from pathlib import Path

import spacy
import pytest
import srsly
from click import NoSuchOption
from packaging.specifiers import SpecifierSet
from thinc.api import Config, ConfigValidationError
from spacy.tokens import DocBin

from weasel.cli.remote_storage import RemoteStorage
from weasel.cli.run import _check_requirements
from weasel.util import load_project_config

from spacy import about
from spacy.cli import info
from spacy.cli._util import walk_directory
from spacy.cli._util import parse_config_overrides, string_to_list
from spacy.cli.debug_data import _compile_gold, _get_labels_from_model
from spacy.cli.debug_data import _get_labels_from_spancat
from spacy.cli.debug_data import _get_distribution, _get_kl_divergence
from spacy.cli.debug_data import _get_span_characteristics
from spacy.cli.debug_data import _print_span_characteristics
from spacy.cli.debug_data import _get_spans_length_freq_dist
from spacy.cli.download import get_compatibility, get_version
from spacy.cli.evaluate import render_parses
from spacy.cli.init_config import RECOMMENDATIONS, init_config, fill_config
from spacy.cli.init_pipeline import _init_labels
from spacy.cli.package import get_third_party_dependencies
from spacy.cli.package import _is_permitted_package_name
from spacy.cli.validate import get_model_pkgs
from spacy.cli.apply import apply
from spacy.cli.find_threshold import find_threshold
from spacy.lang.en import English
from spacy.lang.nl import Dutch
from spacy.language import Language
from spacy.schemas import RecommendationSchema
from spacy.tokens import Doc, DocBin
from spacy.tokens.span import Span
from spacy.training import Example, docs_to_json, offsets_to_biluo_tags
from spacy.training.converters import conll_ner_to_docs, conllu_to_docs
from spacy.training.converters import iob_to_docs
from spacy.util import ENV_VARS, get_minor_version, load_model_from_config, load_config

from .util import make_tempdir


@pytest.mark.issue(4665)
def test_cli_converters_conllu_empty_heads_ner():
    """
    conllu_to_docs should not raise an exception if the HEAD column contains an
    underscore
    """
    input_data = """
1	[	_	PUNCT	-LRB-	_	_	punct	_	_
2	This	_	DET	DT	_	_	det	_	_
3	killing	_	NOUN	NN	_	_	nsubj	_	_
4	of	_	ADP	IN	_	_	case	_	_
5	a	_	DET	DT	_	_	det	_	_
6	respected	_	ADJ	JJ	_	_	amod	_	_
7	cleric	_	NOUN	NN	_	_	nmod	_	_
8	will	_	AUX	MD	_	_	aux	_	_
9	be	_	AUX	VB	_	_	aux	_	_
10	causing	_	VERB	VBG	_	_	root	_	_
11	us	_	PRON	PRP	_	_	iobj	_	_
12	trouble	_	NOUN	NN	_	_	dobj	_	_
13	for	_	ADP	IN	_	_	case	_	_
14	years	_	NOUN	NNS	_	_	nmod	_	_
15	to	_	PART	TO	_	_	mark	_	_
16	come	_	VERB	VB	_	_	acl	_	_
17	.	_	PUNCT	.	_	_	punct	_	_
18	]	_	PUNCT	-RRB-	_	_	punct	_	_
"""
    docs = list(conllu_to_docs(input_data))
    # heads are all 0
    assert not all([t.head.i for t in docs[0]])
    # NER is unset
    assert not docs[0].has_annotation("ENT_IOB")


@pytest.mark.issue(4924)
def test_issue4924():
    nlp = Language()
    example = Example.from_dict(nlp.make_doc(""), {})
    nlp.evaluate([example])


@pytest.mark.issue(7055)
def test_issue7055():
    """Test that fill-config doesn't turn sourced components into factories."""
    source_cfg = {
        "nlp": {"lang": "en", "pipeline": ["tok2vec", "tagger"]},
        "components": {
            "tok2vec": {"factory": "tok2vec"},
            "tagger": {"factory": "tagger"},
        },
    }
    source_nlp = English.from_config(source_cfg)
    with make_tempdir() as dir_path:
        # We need to create a loadable source pipeline
        source_path = dir_path / "test_model"
        source_nlp.to_disk(source_path)
        base_cfg = {
            "nlp": {"lang": "en", "pipeline": ["tok2vec", "tagger", "ner"]},
            "components": {
                "tok2vec": {"source": str(source_path)},
                "tagger": {"source": str(source_path)},
                "ner": {"factory": "ner"},
            },
        }
        base_cfg = Config(base_cfg)
        base_path = dir_path / "base.cfg"
        base_cfg.to_disk(base_path)
        output_path = dir_path / "config.cfg"
        fill_config(output_path, base_path, silent=True)
        filled_cfg = load_config(output_path)
    assert filled_cfg["components"]["tok2vec"]["source"] == str(source_path)
    assert filled_cfg["components"]["tagger"]["source"] == str(source_path)
    assert filled_cfg["components"]["ner"]["factory"] == "ner"
    assert "model" in filled_cfg["components"]["ner"]


@pytest.mark.issue(11235)
def test_issue11235():
    """
    Test that the cli handles interpolation in the directory names correctly when loading project config.
    """
    lang_var = "en"
    variables = {"lang": lang_var}
    commands = [{"name": "x", "script": ["hello ${vars.lang}"]}]
    directories = ["cfg", "${vars.lang}_model"]
    project = {"commands": commands, "vars": variables, "directories": directories}
    with make_tempdir() as d:
        srsly.write_yaml(d / "project.yml", project)
        cfg = load_project_config(d)
        # Check that the directories are interpolated and created correctly
        assert os.path.exists(d / "cfg")
        assert os.path.exists(d / f"{lang_var}_model")
    assert cfg["commands"][0]["script"][0] == f"hello {lang_var}"


@pytest.mark.issue(12566)
@pytest.mark.parametrize(
    "factory,output_file",
    [("deps", "parses.html"), ("ents", "entities.html"), ("spans", "spans.html")],
)
def test_issue12566(factory: str, output_file: str):
    """
    Test if all displaCy types (ents, dep, spans) produce an HTML file
    """
    with make_tempdir() as tmp_dir:
        # Create sample spaCy file
        doc_json = {
            "ents": [
                {"end": 54, "label": "nam_adj_country", "start": 44},
                {"end": 83, "label": "nam_liv_person", "start": 69},
                {"end": 100, "label": "nam_pro_title_book", "start": 86},
            ],
            "spans": {
                "sc": [
                    {"end": 54, "kb_id": "", "label": "nam_adj_country", "start": 44},
                    {"end": 83, "kb_id": "", "label": "nam_liv_person", "start": 69},
                    {
                        "end": 100,
                        "kb_id": "",
                        "label": "nam_pro_title_book",
                        "start": 86,
                    },
                ]
            },
            "text": "Niedawno czytał em nową książkę znakomitego szkockiego medioznawcy , "
            "Briana McNaira - Cultural Chaos .",
            "tokens": [
                # fmt: off
                {"id": 0, "start": 0, "end": 8, "tag": "ADV", "pos": "ADV", "morph": "Degree=Pos", "lemma": "niedawno", "dep": "advmod", "head": 1, },
                {"id": 1, "start": 9, "end": 15, "tag": "PRAET", "pos": "VERB", "morph": "Animacy=Hum|Aspect=Imp|Gender=Masc|Mood=Ind|Number=Sing|Tense=Past|VerbForm=Fin|Voice=Act", "lemma": "czytać", "dep": "ROOT", "head": 1, },
                {"id": 2, "start": 16, "end": 18, "tag": "AGLT", "pos": "NOUN", "morph": "Animacy=Inan|Case=Ins|Gender=Masc|Number=Sing", "lemma": "em", "dep": "iobj", "head": 1, },
                {"id": 3, "start": 19, "end": 23, "tag": "ADJ", "pos": "ADJ", "morph": "Case=Acc|Degree=Pos|Gender=Fem|Number=Sing", "lemma": "nowy", "dep": "amod", "head": 4, },
                {"id": 4, "start": 24, "end": 31, "tag": "SUBST", "pos": "NOUN", "morph": "Case=Acc|Gender=Fem|Number=Sing", "lemma": "książka", "dep": "obj", "head": 1, },
                {"id": 5, "start": 32, "end": 43, "tag": "ADJ", "pos": "ADJ", "morph": "Animacy=Nhum|Case=Gen|Degree=Pos|Gender=Masc|Number=Sing", "lemma": "znakomit", "dep": "acl", "head": 4, },
                {"id": 6, "start": 44, "end": 54, "tag": "ADJ", "pos": "ADJ", "morph": "Animacy=Hum|Case=Gen|Degree=Pos|Gender=Masc|Number=Sing", "lemma": "szkockiy", "dep": "amod", "head": 7, },
                {"id": 7, "start": 55, "end": 66, "tag": "SUBST", "pos": "NOUN", "morph": "Animacy=Hum|Case=Gen|Gender=Masc|Number=Sing", "lemma": "medioznawca", "dep": "iobj", "head": 5, },
                {"id": 8, "start": 67, "end": 68, "tag": "INTERP", "pos": "PUNCT", "morph": "PunctType=Comm", "lemma": ",", "dep": "punct", "head": 9, },
                {"id": 9, "start": 69, "end": 75, "tag": "SUBST", "pos": "PROPN", "morph": "Animacy=Hum|Case=Gen|Gender=Masc|Number=Sing", "lemma": "Brian", "dep": "nmod", "head": 4, },
                {"id": 10, "start": 76, "end": 83, "tag": "SUBST", "pos": "PROPN", "morph": "Animacy=Hum|Case=Gen|Gender=Masc|Number=Sing", "lemma": "McNair", "dep": "flat", "head": 9, },
                {"id": 11, "start": 84, "end": 85, "tag": "INTERP", "pos": "PUNCT", "morph": "PunctType=Dash", "lemma": "-", "dep": "punct", "head": 12, },
                {"id": 12, "start": 86, "end": 94, "tag": "SUBST", "pos": "PROPN", "morph": "Animacy=Inan|Case=Nom|Gender=Masc|Number=Sing", "lemma": "Cultural", "dep": "conj", "head": 4, },
                {"id": 13, "start": 95, "end": 100, "tag": "SUBST", "pos": "NOUN", "morph": "Animacy=Inan|Case=Nom|Gender=Masc|Number=Sing", "lemma": "Chaos", "dep": "flat", "head": 12, },
                {"id": 14, "start": 101, "end": 102, "tag": "INTERP", "pos": "PUNCT", "morph": "PunctType=Peri", "lemma": ".", "dep": "punct", "head": 1, },
                # fmt: on
            ],
        }

        # Create a .spacy file
        nlp = spacy.blank("pl")
        doc = Doc(nlp.vocab).from_json(doc_json)

        # Run the evaluate command and check if the html files exist
        render_parses(
            docs=[doc], output_path=tmp_dir, model_name="", limit=1, **{factory: True}
        )

        assert (tmp_dir / output_file).is_file()


def test_cli_info():
    nlp = Dutch()
    nlp.add_pipe("textcat")
    with make_tempdir() as tmp_dir:
        nlp.to_disk(tmp_dir)
        raw_data = info(tmp_dir, exclude=[""])
        assert raw_data["lang"] == "nl"
        assert raw_data["components"] == ["textcat"]


def test_cli_converters_conllu_to_docs():
    # from NorNE: https://github.com/ltgoslo/norne/blob/3d23274965f513f23aa48455b28b1878dad23c05/ud/nob/no_bokmaal-ud-dev.conllu
    lines = [
        "1\tDommer\tdommer\tNOUN\t_\tDefinite=Ind|Gender=Masc|Number=Sing\t2\tappos\t_\tO",
        "2\tFinn\tFinn\tPROPN\t_\tGender=Masc\t4\tnsubj\t_\tB-PER",
        "3\tEilertsen\tEilertsen\tPROPN\t_\t_\t2\tname\t_\tI-PER",
        "4\tavstår\tavstå\tVERB\t_\tMood=Ind|Tense=Pres|VerbForm=Fin\t0\troot\t_\tO",
    ]
    input_data = "\n".join(lines)
    converted_docs = list(conllu_to_docs(input_data, n_sents=1))
    assert len(converted_docs) == 1
    converted = [docs_to_json(converted_docs)]
    assert converted[0]["id"] == 0
    assert len(converted[0]["paragraphs"]) == 1
    assert len(converted[0]["paragraphs"][0]["sentences"]) == 1
    sent = converted[0]["paragraphs"][0]["sentences"][0]
    assert len(sent["tokens"]) == 4
    tokens = sent["tokens"]
    assert [t["orth"] for t in tokens] == ["Dommer", "Finn", "Eilertsen", "avstår"]
    assert [t["tag"] for t in tokens] == ["NOUN", "PROPN", "PROPN", "VERB"]
    assert [t["head"] for t in tokens] == [1, 2, -1, 0]
    assert [t["dep"] for t in tokens] == ["appos", "nsubj", "name", "ROOT"]
    ent_offsets = [
        (e[0], e[1], e[2]) for e in converted[0]["paragraphs"][0]["entities"]
    ]
    biluo_tags = offsets_to_biluo_tags(converted_docs[0], ent_offsets, missing="O")
    assert biluo_tags == ["O", "B-PER", "L-PER", "O"]


@pytest.mark.parametrize(
    "lines",
    [
        (
            "1\tDommer\tdommer\tNOUN\t_\tDefinite=Ind|Gender=Masc|Number=Sing\t2\tappos\t_\tname=O",
            "2\tFinn\tFinn\tPROPN\t_\tGender=Masc\t4\tnsubj\t_\tSpaceAfter=No|name=B-PER",
            "3\tEilertsen\tEilertsen\tPROPN\t_\t_\t2\tname\t_\tname=I-PER",
            "4\tavstår\tavstå\tVERB\t_\tMood=Ind|Tense=Pres|VerbForm=Fin\t0\troot\t_\tSpaceAfter=No|name=O",
            "5\t.\t$.\tPUNCT\t_\t_\t4\tpunct\t_\tname=B-BAD",
        ),
        (
            "1\tDommer\tdommer\tNOUN\t_\tDefinite=Ind|Gender=Masc|Number=Sing\t2\tappos\t_\t_",
            "2\tFinn\tFinn\tPROPN\t_\tGender=Masc\t4\tnsubj\t_\tSpaceAfter=No|NE=B-PER",
            "3\tEilertsen\tEilertsen\tPROPN\t_\t_\t2\tname\t_\tNE=L-PER",
            "4\tavstår\tavstå\tVERB\t_\tMood=Ind|Tense=Pres|VerbForm=Fin\t0\troot\t_\tSpaceAfter=No",
            "5\t.\t$.\tPUNCT\t_\t_\t4\tpunct\t_\tNE=B-BAD",
        ),
    ],
)
def test_cli_converters_conllu_to_docs_name_ner_map(lines):
    input_data = "\n".join(lines)
    converted_docs = list(
        conllu_to_docs(input_data, n_sents=1, ner_map={"PER": "PERSON", "BAD": ""})
    )
    assert len(converted_docs) == 1
    converted = [docs_to_json(converted_docs)]
    assert converted[0]["id"] == 0
    assert len(converted[0]["paragraphs"]) == 1
    assert converted[0]["paragraphs"][0]["raw"] == "Dommer FinnEilertsen avstår. "
    assert len(converted[0]["paragraphs"][0]["sentences"]) == 1
    sent = converted[0]["paragraphs"][0]["sentences"][0]
    assert len(sent["tokens"]) == 5
    tokens = sent["tokens"]
    assert [t["orth"] for t in tokens] == ["Dommer", "Finn", "Eilertsen", "avstår", "."]
    assert [t["tag"] for t in tokens] == ["NOUN", "PROPN", "PROPN", "VERB", "PUNCT"]
    assert [t["head"] for t in tokens] == [1, 2, -1, 0, -1]
    assert [t["dep"] for t in tokens] == ["appos", "nsubj", "name", "ROOT", "punct"]
    ent_offsets = [
        (e[0], e[1], e[2]) for e in converted[0]["paragraphs"][0]["entities"]
    ]
    biluo_tags = offsets_to_biluo_tags(converted_docs[0], ent_offsets, missing="O")
    assert biluo_tags == ["O", "B-PERSON", "L-PERSON", "O", "O"]


def test_cli_converters_conllu_to_docs_subtokens():
    # https://raw.githubusercontent.com/ohenrik/nb_news_ud_sm/master/original_data/no-ud-dev-ner.conllu
    lines = [
        "1\tDommer\tdommer\tNOUN\t_\tDefinite=Ind|Gender=Masc|Number=Sing\t2\tappos\t_\tname=O",
        "2-3\tFE\t_\t_\t_\t_\t_\t_\t_\t_",
        "2\tFinn\tFinn\tPROPN\t_\tGender=Masc\t4\tnsubj\t_\tname=B-PER",
        "3\tEilertsen\tEilertsen\tX\t_\tGender=Fem|Tense=past\t2\tname\t_\tname=I-PER",
        "4\tavstår\tavstå\tVERB\t_\tMood=Ind|Tense=Pres|VerbForm=Fin\t0\troot\t_\tSpaceAfter=No|name=O",
        "5\t.\t$.\tPUNCT\t_\t_\t4\tpunct\t_\tname=O",
    ]
    input_data = "\n".join(lines)
    converted_docs = list(
        conllu_to_docs(
            input_data, n_sents=1, merge_subtokens=True, append_morphology=True
        )
    )
    assert len(converted_docs) == 1
    converted = [docs_to_json(converted_docs)]

    assert converted[0]["id"] == 0
    assert len(converted[0]["paragraphs"]) == 1
    assert converted[0]["paragraphs"][0]["raw"] == "Dommer FE avstår. "
    assert len(converted[0]["paragraphs"][0]["sentences"]) == 1
    sent = converted[0]["paragraphs"][0]["sentences"][0]
    assert len(sent["tokens"]) == 4
    tokens = sent["tokens"]
    assert [t["orth"] for t in tokens] == ["Dommer", "FE", "avstår", "."]
    assert [t["tag"] for t in tokens] == [
        "NOUN__Definite=Ind|Gender=Masc|Number=Sing",
        "PROPN_X__Gender=Fem,Masc|Tense=past",
        "VERB__Mood=Ind|Tense=Pres|VerbForm=Fin",
        "PUNCT",
    ]
    assert [t["pos"] for t in tokens] == ["NOUN", "PROPN", "VERB", "PUNCT"]
    assert [t["morph"] for t in tokens] == [
        "Definite=Ind|Gender=Masc|Number=Sing",
        "Gender=Fem,Masc|Tense=past",
        "Mood=Ind|Tense=Pres|VerbForm=Fin",
        "",
    ]
    assert [t["lemma"] for t in tokens] == ["dommer", "Finn Eilertsen", "avstå", "$."]
    assert [t["head"] for t in tokens] == [1, 1, 0, -1]
    assert [t["dep"] for t in tokens] == ["appos", "nsubj", "ROOT", "punct"]
    ent_offsets = [
        (e[0], e[1], e[2]) for e in converted[0]["paragraphs"][0]["entities"]
    ]
    biluo_tags = offsets_to_biluo_tags(converted_docs[0], ent_offsets, missing="O")
    assert biluo_tags == ["O", "U-PER", "O", "O"]


def test_cli_converters_iob_to_docs():
    lines = [
        "I|O like|O London|I-GPE and|O New|B-GPE York|I-GPE City|I-GPE .|O",
        "I|O like|O London|B-GPE and|O New|B-GPE York|I-GPE City|I-GPE .|O",
        "I|PRP|O like|VBP|O London|NNP|I-GPE and|CC|O New|NNP|B-GPE York|NNP|I-GPE City|NNP|I-GPE .|.|O",
        "I|PRP|O like|VBP|O London|NNP|B-GPE and|CC|O New|NNP|B-GPE York|NNP|I-GPE City|NNP|I-GPE .|.|O",
    ]
    input_data = "\n".join(lines)
    converted_docs = list(iob_to_docs(input_data, n_sents=10))
    assert len(converted_docs) == 1
    converted = docs_to_json(converted_docs)
    assert converted["id"] == 0
    assert len(converted["paragraphs"]) == 1
    assert len(converted["paragraphs"][0]["sentences"]) == 4
    for i in range(0, 4):
        sent = converted["paragraphs"][0]["sentences"][i]
        assert len(sent["tokens"]) == 8
        tokens = sent["tokens"]
        expected = ["I", "like", "London", "and", "New", "York", "City", "."]
        assert [t["orth"] for t in tokens] == expected
    assert len(converted_docs[0].ents) == 8
    for ent in converted_docs[0].ents:
        assert ent.text in ["New York City", "London"]


def test_cli_converters_conll_ner_to_docs():
    lines = [
        "-DOCSTART- -X- O O",
        "",
        "I\tO",
        "like\tO",
        "London\tB-GPE",
        "and\tO",
        "New\tB-GPE",
        "York\tI-GPE",
        "City\tI-GPE",
        ".\tO",
        "",
        "I O",
        "like O",
        "London B-GPE",
        "and O",
        "New B-GPE",
        "York I-GPE",
        "City I-GPE",
        ". O",
        "",
        "I PRP O",
        "like VBP O",
        "London NNP B-GPE",
        "and CC O",
        "New NNP B-GPE",
        "York NNP I-GPE",
        "City NNP I-GPE",
        ". . O",
        "",
        "I PRP _ O",
        "like VBP _ O",
        "London NNP _ B-GPE",
        "and CC _ O",
        "New NNP _ B-GPE",
        "York NNP _ I-GPE",
        "City NNP _ I-GPE",
        ". . _ O",
        "",
        "I\tPRP\t_\tO",
        "like\tVBP\t_\tO",
        "London\tNNP\t_\tB-GPE",
        "and\tCC\t_\tO",
        "New\tNNP\t_\tB-GPE",
        "York\tNNP\t_\tI-GPE",
        "City\tNNP\t_\tI-GPE",
        ".\t.\t_\tO",
    ]
    input_data = "\n".join(lines)
    converted_docs = list(conll_ner_to_docs(input_data, n_sents=10))
    assert len(converted_docs) == 1
    converted = docs_to_json(converted_docs)
    assert converted["id"] == 0
    assert len(converted["paragraphs"]) == 1
    assert len(converted["paragraphs"][0]["sentences"]) == 5
    for i in range(0, 5):
        sent = converted["paragraphs"][0]["sentences"][i]
        assert len(sent["tokens"]) == 8
        tokens = sent["tokens"]
        # fmt: off
        assert [t["orth"] for t in tokens] == ["I", "like", "London", "and", "New", "York", "City", "."]
        # fmt: on
    assert len(converted_docs[0].ents) == 10
    for ent in converted_docs[0].ents:
        assert ent.text in ["New York City", "London"]


@pytest.mark.parametrize(
    "args,expected",
    [
        # fmt: off
        (["--x.foo", "10"], {"x.foo": 10}),
        (["--x.foo=10"], {"x.foo": 10}),
        (["--x.foo", "bar"], {"x.foo": "bar"}),
        (["--x.foo=bar"], {"x.foo": "bar"}),
        (["--x.foo", "--x.bar", "baz"], {"x.foo": True, "x.bar": "baz"}),
        (["--x.foo", "--x.bar=baz"], {"x.foo": True, "x.bar": "baz"}),
        (["--x.foo", "10.1", "--x.bar", "--x.baz", "false"], {"x.foo": 10.1, "x.bar": True, "x.baz": False}),
        (["--x.foo", "10.1", "--x.bar", "--x.baz=false"], {"x.foo": 10.1, "x.bar": True, "x.baz": False})
        # fmt: on
    ],
)
def test_parse_config_overrides(args, expected):
    assert parse_config_overrides(args) == expected


@pytest.mark.parametrize("args", [["--foo"], ["--x.foo", "bar", "--baz"]])
def test_parse_config_overrides_invalid(args):
    with pytest.raises(NoSuchOption):
        parse_config_overrides(args)


@pytest.mark.parametrize("args", [["--x.foo", "bar", "baz"], ["x.foo"]])
def test_parse_config_overrides_invalid_2(args):
    with pytest.raises(SystemExit):
        parse_config_overrides(args)


def test_parse_cli_overrides():
    overrides = "--x.foo bar --x.bar=12 --x.baz false --y.foo=hello"
    os.environ[ENV_VARS.CONFIG_OVERRIDES] = overrides
    result = parse_config_overrides([])
    assert len(result) == 4
    assert result["x.foo"] == "bar"
    assert result["x.bar"] == 12
    assert result["x.baz"] is False
    assert result["y.foo"] == "hello"
    os.environ[ENV_VARS.CONFIG_OVERRIDES] = "--x"
    assert parse_config_overrides([], env_var=None) == {}
    with pytest.raises(SystemExit):
        parse_config_overrides([])
    os.environ[ENV_VARS.CONFIG_OVERRIDES] = "hello world"
    with pytest.raises(SystemExit):
        parse_config_overrides([])
    del os.environ[ENV_VARS.CONFIG_OVERRIDES]


@pytest.mark.parametrize("lang", ["en", "nl"])
@pytest.mark.parametrize(
    "pipeline",
    [
        ["tagger", "parser", "ner"],
        [],
        ["ner", "textcat", "sentencizer"],
        ["morphologizer", "spancat", "entity_linker"],
        ["spancat_singlelabel", "textcat_multilabel"],
    ],
)
@pytest.mark.parametrize("optimize", ["efficiency", "accuracy"])
@pytest.mark.parametrize("pretraining", [True, False])
def test_init_config(lang, pipeline, optimize, pretraining):
    # TODO: add more tests and also check for GPU with transformers
    config = init_config(
        lang=lang,
        pipeline=pipeline,
        optimize=optimize,
        pretraining=pretraining,
        gpu=False,
    )
    assert isinstance(config, Config)
    if pretraining:
        config["paths"]["raw_text"] = "my_data.jsonl"
    load_model_from_config(config, auto_fill=True)


def test_model_recommendations():
    for lang, data in RECOMMENDATIONS.items():
        assert RecommendationSchema(**data)


@pytest.mark.parametrize(
    "value",
    [
        # fmt: off
        "parser,textcat,tagger",
        " parser, textcat ,tagger ",
        'parser,textcat,tagger',
        ' parser, textcat ,tagger ',
        ' "parser"," textcat " ,"tagger "',
        " 'parser',' textcat ' ,'tagger '",
        '[parser,textcat,tagger]',
        '["parser","textcat","tagger"]',
        '[" parser" ,"textcat ", " tagger " ]',
        "[parser,textcat,tagger]",
        "[ parser, textcat , tagger]",
        "['parser','textcat','tagger']",
        "[' parser' , 'textcat', ' tagger ' ]",
        # fmt: on
    ],
)
def test_string_to_list(value):
    assert string_to_list(value, intify=False) == ["parser", "textcat", "tagger"]


@pytest.mark.parametrize(
    "value",
    [
        # fmt: off
        "1,2,3",
        '[1,2,3]',
        '["1","2","3"]',
        '[" 1" ,"2 ", " 3 " ]',
        "[' 1' , '2', ' 3 ' ]",
        # fmt: on
    ],
)
def test_string_to_list_intify(value):
    assert string_to_list(value, intify=False) == ["1", "2", "3"]
    assert string_to_list(value, intify=True) == [1, 2, 3]


def test_download_compatibility():
    spec = SpecifierSet("==" + about.__version__)
    spec.prereleases = False
    if about.__version__ in spec:
        model_name = "en_core_web_sm"
        compatibility = get_compatibility()
        version = get_version(model_name, compatibility)
        assert get_minor_version(about.__version__) == get_minor_version(version)


def test_validate_compatibility_table():
    spec = SpecifierSet("==" + about.__version__)
    spec.prereleases = False
    if about.__version__ in spec:
        model_pkgs, compat = get_model_pkgs()
        spacy_version = get_minor_version(about.__version__)
        current_compat = compat.get(spacy_version, {})
        assert len(current_compat) > 0
        assert "en_core_web_sm" in current_compat


@pytest.mark.parametrize("component_name", ["ner", "textcat", "spancat", "tagger"])
def test_init_labels(component_name):
    nlp = Dutch()
    component = nlp.add_pipe(component_name)
    for label in ["T1", "T2", "T3", "T4"]:
        component.add_label(label)
    assert len(nlp.get_pipe(component_name).labels) == 4

    with make_tempdir() as tmp_dir:
        _init_labels(nlp, tmp_dir)

        config = init_config(
            lang="nl",
            pipeline=[component_name],
            optimize="efficiency",
            gpu=False,
        )
        config["initialize"]["components"][component_name] = {
            "labels": {
                "@readers": "spacy.read_labels.v1",
                "path": f"{tmp_dir}/{component_name}.json",
            }
        }

        nlp2 = load_model_from_config(config, auto_fill=True)
        assert len(nlp2.get_pipe(component_name).labels) == 0
        nlp2.initialize()
        assert len(nlp2.get_pipe(component_name).labels) == 4


def test_get_third_party_dependencies():
    # We can't easily test the detection of third-party packages here, but we
    # can at least make sure that the function and its importlib magic runs.
    nlp = Dutch()
    # Test with component factory based on Cython module
    nlp.add_pipe("tagger")
    assert get_third_party_dependencies(nlp.config) == []

    # Test with legacy function
    nlp = Dutch()
    nlp.add_pipe(
        "textcat",
        config={
            "model": {
                # Do not update from legacy architecture spacy.TextCatBOW.v1
                "@architectures": "spacy.TextCatBOW.v1",
                "exclusive_classes": True,
                "ngram_size": 1,
                "no_output_layer": False,
            }
        },
    )
    assert get_third_party_dependencies(nlp.config) == []

    # Test with lang-specific factory
    @Dutch.factory("third_party_test")
    def test_factory(nlp, name):
        return lambda x: x

    nlp.add_pipe("third_party_test")
    # Before #9674 this would throw an exception
    get_third_party_dependencies(nlp.config)


@pytest.mark.slow
@pytest.mark.parametrize(
    "factory_name,pipe_name",
    [
        ("ner", "ner"),
        ("ner", "my_ner"),
        ("spancat", "spancat"),
        ("spancat", "my_spancat"),
    ],
)
def test_get_labels_from_model(factory_name, pipe_name):
    labels = ("A", "B")

    nlp = English()
    pipe = nlp.add_pipe(factory_name, name=pipe_name)
    for label in labels:
        pipe.add_label(label)
    nlp.initialize()
    assert nlp.get_pipe(pipe_name).labels == labels
    if factory_name == "spancat":
        assert _get_labels_from_spancat(nlp)[pipe.key] == set(labels)
    else:
        assert _get_labels_from_model(nlp, factory_name) == set(labels)


def test_permitted_package_names():
    # https://www.python.org/dev/peps/pep-0426/#name
    assert _is_permitted_package_name("Meine_Bäume") == False
    assert _is_permitted_package_name("_package") == False
    assert _is_permitted_package_name("package_") == False
    assert _is_permitted_package_name(".package") == False
    assert _is_permitted_package_name("package.") == False
    assert _is_permitted_package_name("-package") == False
    assert _is_permitted_package_name("package-") == False


def test_debug_data_compile_gold():
    nlp = English()
    pred = Doc(nlp.vocab, words=["Token", ".", "New", "York", "City"])
    ref = Doc(
        nlp.vocab,
        words=["Token", ".", "New York City"],
        sent_starts=[True, False, True],
        ents=["O", "O", "B-ENT"],
    )
    eg = Example(pred, ref)
    data = _compile_gold([eg], ["ner"], nlp, True)
    assert data["boundary_cross_ents"] == 0

    pred = Doc(nlp.vocab, words=["Token", ".", "New", "York", "City"])
    ref = Doc(
        nlp.vocab,
        words=["Token", ".", "New York City"],
        sent_starts=[True, False, True],
        ents=["O", "B-ENT", "I-ENT"],
    )
    eg = Example(pred, ref)
    data = _compile_gold([eg], ["ner"], nlp, True)
    assert data["boundary_cross_ents"] == 1


def test_debug_data_compile_gold_for_spans():
    nlp = English()
    spans_key = "sc"

    pred = Doc(nlp.vocab, words=["Welcome", "to", "the", "Bank", "of", "China", "."])
    pred.spans[spans_key] = [Span(pred, 3, 6, "ORG"), Span(pred, 5, 6, "GPE")]
    ref = Doc(nlp.vocab, words=["Welcome", "to", "the", "Bank", "of", "China", "."])
    ref.spans[spans_key] = [Span(ref, 3, 6, "ORG"), Span(ref, 5, 6, "GPE")]
    eg = Example(pred, ref)

    data = _compile_gold([eg], ["spancat"], nlp, True)

    assert data["spancat"][spans_key] == Counter({"ORG": 1, "GPE": 1})
    assert data["spans_length"][spans_key] == {"ORG": [3], "GPE": [1]}
    assert data["spans_per_type"][spans_key] == {
        "ORG": [Span(ref, 3, 6, "ORG")],
        "GPE": [Span(ref, 5, 6, "GPE")],
    }
    assert data["sb_per_type"][spans_key] == {
        "ORG": {"start": [ref[2:3]], "end": [ref[6:7]]},
        "GPE": {"start": [ref[4:5]], "end": [ref[6:7]]},
    }


def test_frequency_distribution_is_correct():
    nlp = English()
    docs = [
        Doc(nlp.vocab, words=["Bank", "of", "China"]),
        Doc(nlp.vocab, words=["China"]),
    ]

    expected = Counter({"china": 0.5, "bank": 0.25, "of": 0.25})
    freq_distribution = _get_distribution(docs, normalize=True)
    assert freq_distribution == expected


def test_kl_divergence_computation_is_correct():
    p = Counter({"a": 0.5, "b": 0.25})
    q = Counter({"a": 0.25, "b": 0.50, "c": 0.15, "d": 0.10})
    result = _get_kl_divergence(p, q)
    expected = 0.1733
    assert math.isclose(result, expected, rel_tol=1e-3)


def test_get_span_characteristics_return_value():
    nlp = English()
    spans_key = "sc"

    pred = Doc(nlp.vocab, words=["Welcome", "to", "the", "Bank", "of", "China", "."])
    pred.spans[spans_key] = [Span(pred, 3, 6, "ORG"), Span(pred, 5, 6, "GPE")]
    ref = Doc(nlp.vocab, words=["Welcome", "to", "the", "Bank", "of", "China", "."])
    ref.spans[spans_key] = [Span(ref, 3, 6, "ORG"), Span(ref, 5, 6, "GPE")]
    eg = Example(pred, ref)

    examples = [eg]
    data = _compile_gold(examples, ["spancat"], nlp, True)
    span_characteristics = _get_span_characteristics(
        examples=examples, compiled_gold=data, spans_key=spans_key
    )

    assert {"sd", "bd", "lengths"}.issubset(span_characteristics.keys())
    assert span_characteristics["min_length"] == 1
    assert span_characteristics["max_length"] == 3


def test_ensure_print_span_characteristics_wont_fail():
    """Test if interface between two methods aren't destroyed if refactored"""
    nlp = English()
    spans_key = "sc"

    pred = Doc(nlp.vocab, words=["Welcome", "to", "the", "Bank", "of", "China", "."])
    pred.spans[spans_key] = [Span(pred, 3, 6, "ORG"), Span(pred, 5, 6, "GPE")]
    ref = Doc(nlp.vocab, words=["Welcome", "to", "the", "Bank", "of", "China", "."])
    ref.spans[spans_key] = [Span(ref, 3, 6, "ORG"), Span(ref, 5, 6, "GPE")]
    eg = Example(pred, ref)

    examples = [eg]
    data = _compile_gold(examples, ["spancat"], nlp, True)
    span_characteristics = _get_span_characteristics(
        examples=examples, compiled_gold=data, spans_key=spans_key
    )
    _print_span_characteristics(span_characteristics)


@pytest.mark.parametrize("threshold", [70, 80, 85, 90, 95])
def test_span_length_freq_dist_threshold_must_be_correct(threshold):
    sample_span_lengths = {
        "span_type_1": [1, 4, 4, 5],
        "span_type_2": [5, 3, 3, 2],
        "span_type_3": [3, 1, 3, 3],
    }
    span_freqs = _get_spans_length_freq_dist(sample_span_lengths, threshold)
    assert sum(span_freqs.values()) >= threshold


def test_span_length_freq_dist_output_must_be_correct():
    sample_span_lengths = {
        "span_type_1": [1, 4, 4, 5],
        "span_type_2": [5, 3, 3, 2],
        "span_type_3": [3, 1, 3, 3],
    }
    threshold = 90
    span_freqs = _get_spans_length_freq_dist(sample_span_lengths, threshold)
    assert sum(span_freqs.values()) >= threshold
    assert list(span_freqs.keys()) == [3, 1, 4, 5, 2]


def test_applycli_empty_dir():
    with make_tempdir() as data_path:
        output = data_path / "test.spacy"
        apply(data_path, output, "blank:en", "text", 1, 1)


def test_applycli_docbin():
    with make_tempdir() as data_path:
        output = data_path / "testout.spacy"
        nlp = spacy.blank("en")
        doc = nlp("testing apply cli.")
        # test empty DocBin case
        docbin = DocBin()
        docbin.to_disk(data_path / "testin.spacy")
        apply(data_path, output, "blank:en", "text", 1, 1)
        docbin.add(doc)
        docbin.to_disk(data_path / "testin.spacy")
        apply(data_path, output, "blank:en", "text", 1, 1)


def test_applycli_jsonl():
    with make_tempdir() as data_path:
        output = data_path / "testout.spacy"
        data = [{"field": "Testing apply cli.", "key": 234}]
        data2 = [{"field": "234"}]
        srsly.write_jsonl(data_path / "test.jsonl", data)
        apply(data_path, output, "blank:en", "field", 1, 1)
        srsly.write_jsonl(data_path / "test2.jsonl", data2)
        apply(data_path, output, "blank:en", "field", 1, 1)


def test_applycli_txt():
    with make_tempdir() as data_path:
        output = data_path / "testout.spacy"
        with open(data_path / "test.foo", "w") as ftest:
            ftest.write("Testing apply cli.")
        apply(data_path, output, "blank:en", "text", 1, 1)


def test_applycli_mixed():
    with make_tempdir() as data_path:
        output = data_path / "testout.spacy"
        text = "Testing apply cli"
        nlp = spacy.blank("en")
        doc = nlp(text)
        jsonl_data = [{"text": text}]
        srsly.write_jsonl(data_path / "test.jsonl", jsonl_data)
        docbin = DocBin()
        docbin.add(doc)
        docbin.to_disk(data_path / "testin.spacy")
        with open(data_path / "test.txt", "w") as ftest:
            ftest.write(text)
        apply(data_path, output, "blank:en", "text", 1, 1)
        # Check whether it worked
        result = list(DocBin().from_disk(output).get_docs(nlp.vocab))
        assert len(result) == 3
        for doc in result:
            assert doc.text == text


def test_applycli_user_data():
    Doc.set_extension("ext", default=0)
    val = ("ext", 0)
    with make_tempdir() as data_path:
        output = data_path / "testout.spacy"
        nlp = spacy.blank("en")
        doc = nlp("testing apply cli.")
        doc._.ext = val
        docbin = DocBin(store_user_data=True)
        docbin.add(doc)
        docbin.to_disk(data_path / "testin.spacy")
        apply(data_path, output, "blank:en", "", 1, 1)
        result = list(DocBin().from_disk(output).get_docs(nlp.vocab))
        assert result[0]._.ext == val


def test_cli_find_threshold(capsys):
    def make_examples(nlp: Language) -> List[Example]:
        docs: List[Example] = []

        for t in [
            (
                "I am angry and confused in the Bank of America.",
                {
                    "cats": {"ANGRY": 1.0, "CONFUSED": 1.0, "HAPPY": 0.0},
                    "spans": {"sc": [(31, 46, "ORG")]},
                },
            ),
            (
                "I am confused but happy in New York.",
                {
                    "cats": {"ANGRY": 0.0, "CONFUSED": 1.0, "HAPPY": 1.0},
                    "spans": {"sc": [(27, 35, "GPE")]},
                },
            ),
        ]:
            doc = nlp.make_doc(t[0])
            docs.append(Example.from_dict(doc, t[1]))

        return docs

    def init_nlp(
        components: Tuple[Tuple[str, Dict[str, Any]], ...] = ()
    ) -> Tuple[Language, List[Example]]:
        new_nlp = English()
        new_nlp.add_pipe(  # type: ignore
            factory_name="textcat_multilabel",
            name="tc_multi",
            config={"threshold": 0.9},
        )

        # Append additional components to pipeline.
        for cfn, comp_config in components:
            new_nlp.add_pipe(cfn, config=comp_config)

        new_examples = make_examples(new_nlp)
        new_nlp.initialize(get_examples=lambda: new_examples)
        for i in range(5):
            new_nlp.update(new_examples)

        return new_nlp, new_examples

    with make_tempdir() as docs_dir:
        # Check whether find_threshold() identifies lowest threshold above 0 as (first) ideal threshold, as this matches
        # the current model behavior with the examples above. This can break once the model behavior changes and serves
        # mostly as a smoke test.
        nlp, examples = init_nlp()
        DocBin(docs=[example.reference for example in examples]).to_disk(
            docs_dir / "docs.spacy"
        )
        with make_tempdir() as nlp_dir:
            nlp.to_disk(nlp_dir)
            best_threshold, best_score, res = find_threshold(
                model=nlp_dir,
                data_path=docs_dir / "docs.spacy",
                pipe_name="tc_multi",
                threshold_key="threshold",
                scores_key="cats_macro_f",
                silent=True,
            )
            assert best_score == max(res.values())
            assert res[1.0] == 0.0

        # Test with spancat.
        nlp, _ = init_nlp((("spancat", {}),))
        with make_tempdir() as nlp_dir:
            nlp.to_disk(nlp_dir)
            best_threshold, best_score, res = find_threshold(
                model=nlp_dir,
                data_path=docs_dir / "docs.spacy",
                pipe_name="spancat",
                threshold_key="threshold",
                scores_key="spans_sc_f",
                silent=True,
            )
            assert best_score == max(res.values())
            assert res[1.0] == 0.0

        # Having multiple textcat_multilabel components should work, since the name has to be specified.
        nlp, _ = init_nlp((("textcat_multilabel", {}),))
        with make_tempdir() as nlp_dir:
            nlp.to_disk(nlp_dir)
            assert find_threshold(
                model=nlp_dir,
                data_path=docs_dir / "docs.spacy",
                pipe_name="tc_multi",
                threshold_key="threshold",
                scores_key="cats_macro_f",
                silent=True,
            )

        # Specifying the name of an non-existing pipe should fail.
        nlp, _ = init_nlp()
        with make_tempdir() as nlp_dir:
            nlp.to_disk(nlp_dir)
            with pytest.raises(AttributeError):
                find_threshold(
                    model=nlp_dir,
                    data_path=docs_dir / "docs.spacy",
                    pipe_name="_",
                    threshold_key="threshold",
                    scores_key="cats_macro_f",
                    silent=True,
                )


def test_walk_directory():
    with make_tempdir() as d:
        files = [
            "data1.iob",
            "data2.iob",
            "data3.json",
            "data4.conll",
            "data5.conll",
            "data6.conll",
            "data7.txt",
        ]

        for f in files:
            Path(d / f).touch()

        assert (len(walk_directory(d))) == 7
        assert (len(walk_directory(d, suffix=None))) == 7
        assert (len(walk_directory(d, suffix="json"))) == 1
        assert (len(walk_directory(d, suffix="iob"))) == 2
        assert (len(walk_directory(d, suffix="conll"))) == 3
        assert (len(walk_directory(d, suffix="pdf"))) == 0


def test_debug_data_trainable_lemmatizer_basic():
    examples = [
        ("She likes green eggs", {"lemmas": ["she", "like", "green", "egg"]}),
        ("Eat blue ham", {"lemmas": ["eat", "blue", "ham"]}),
    ]
    nlp = Language()
    train_examples = []
    for t in examples:
        train_examples.append(Example.from_dict(nlp.make_doc(t[0]), t[1]))

    data = _compile_gold(train_examples, ["trainable_lemmatizer"], nlp, True)
    # ref test_edit_tree_lemmatizer::test_initialize_from_labels
    # this results in 4 trees
    assert len(data["lemmatizer_trees"]) == 4


def test_debug_data_trainable_lemmatizer_partial():
    partial_examples = [
        # partial annotation
        ("She likes green eggs", {"lemmas": ["", "like", "green", ""]}),
        # misaligned partial annotation
        (
            "He hates green eggs",
            {
                "words": ["He", "hat", "es", "green", "eggs"],
                "lemmas": ["", "hat", "e", "green", ""],
            },
        ),
    ]
    nlp = Language()
    train_examples = []
    for t in partial_examples:
        train_examples.append(Example.from_dict(nlp.make_doc(t[0]), t[1]))

    data = _compile_gold(train_examples, ["trainable_lemmatizer"], nlp, True)
    assert data["partial_lemma_annotations"] == 2


def test_debug_data_trainable_lemmatizer_low_cardinality():
    low_cardinality_examples = [
        ("She likes green eggs", {"lemmas": ["no", "no", "no", "no"]}),
        ("Eat blue ham", {"lemmas": ["no", "no", "no"]}),
    ]
    nlp = Language()
    train_examples = []
    for t in low_cardinality_examples:
        train_examples.append(Example.from_dict(nlp.make_doc(t[0]), t[1]))

    data = _compile_gold(train_examples, ["trainable_lemmatizer"], nlp, True)
    assert data["n_low_cardinality_lemmas"] == 2


def test_debug_data_trainable_lemmatizer_not_annotated():
    unannotated_examples = [
        ("She likes green eggs", {}),
        ("Eat blue ham", {}),
    ]
    nlp = Language()
    train_examples = []
    for t in unannotated_examples:
        train_examples.append(Example.from_dict(nlp.make_doc(t[0]), t[1]))

    data = _compile_gold(train_examples, ["trainable_lemmatizer"], nlp, True)
    assert data["no_lemma_annotations"] == 2
