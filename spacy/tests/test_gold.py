# coding: utf-8
from __future__ import unicode_literals

from spacy.gold import biluo_tags_from_offsets, offsets_from_biluo_tags
from spacy.gold import spans_from_biluo_tags, GoldParse, iob_to_biluo
from spacy.gold import GoldCorpus, docs_to_json
from spacy.lang.en import English
from spacy.tokens import Doc
from spacy.util import compounding, minibatch
from .util import make_tempdir
import pytest
import srsly


def test_gold_biluo_U(en_vocab):
    words = ["I", "flew", "to", "London", "."]
    spaces = [True, True, True, False, True]
    doc = Doc(en_vocab, words=words, spaces=spaces)
    entities = [(len("I flew to "), len("I flew to London"), "LOC")]
    tags = biluo_tags_from_offsets(doc, entities)
    assert tags == ["O", "O", "O", "U-LOC", "O"]


def test_gold_biluo_BL(en_vocab):
    words = ["I", "flew", "to", "San", "Francisco", "."]
    spaces = [True, True, True, True, False, True]
    doc = Doc(en_vocab, words=words, spaces=spaces)
    entities = [(len("I flew to "), len("I flew to San Francisco"), "LOC")]
    tags = biluo_tags_from_offsets(doc, entities)
    assert tags == ["O", "O", "O", "B-LOC", "L-LOC", "O"]


def test_gold_biluo_BIL(en_vocab):
    words = ["I", "flew", "to", "San", "Francisco", "Valley", "."]
    spaces = [True, True, True, True, True, False, True]
    doc = Doc(en_vocab, words=words, spaces=spaces)
    entities = [(len("I flew to "), len("I flew to San Francisco Valley"), "LOC")]
    tags = biluo_tags_from_offsets(doc, entities)
    assert tags == ["O", "O", "O", "B-LOC", "I-LOC", "L-LOC", "O"]


def test_gold_biluo_overlap(en_vocab):
    words = ["I", "flew", "to", "San", "Francisco", "Valley", "."]
    spaces = [True, True, True, True, True, False, True]
    doc = Doc(en_vocab, words=words, spaces=spaces)
    entities = [
        (len("I flew to "), len("I flew to San Francisco Valley"), "LOC"),
        (len("I flew to "), len("I flew to San Francisco"), "LOC"),
    ]
    with pytest.raises(ValueError):
        biluo_tags_from_offsets(doc, entities)


def test_gold_biluo_misalign(en_vocab):
    words = ["I", "flew", "to", "San", "Francisco", "Valley."]
    spaces = [True, True, True, True, True, False]
    doc = Doc(en_vocab, words=words, spaces=spaces)
    entities = [(len("I flew to "), len("I flew to San Francisco Valley"), "LOC")]
    tags = biluo_tags_from_offsets(doc, entities)
    assert tags == ["O", "O", "O", "-", "-", "-"]


def test_roundtrip_offsets_biluo_conversion(en_tokenizer):
    text = "I flew to Silicon Valley via London."
    biluo_tags = ["O", "O", "O", "B-LOC", "L-LOC", "O", "U-GPE", "O"]
    offsets = [(10, 24, "LOC"), (29, 35, "GPE")]
    doc = en_tokenizer(text)
    biluo_tags_converted = biluo_tags_from_offsets(doc, offsets)
    assert biluo_tags_converted == biluo_tags
    offsets_converted = offsets_from_biluo_tags(doc, biluo_tags)
    assert offsets_converted == offsets


def test_biluo_spans(en_tokenizer):
    doc = en_tokenizer("I flew to Silicon Valley via London.")
    biluo_tags = ["O", "O", "O", "B-LOC", "L-LOC", "O", "U-GPE", "O"]
    spans = spans_from_biluo_tags(doc, biluo_tags)
    assert len(spans) == 2
    assert spans[0].text == "Silicon Valley"
    assert spans[0].label_ == "LOC"
    assert spans[1].text == "London"
    assert spans[1].label_ == "GPE"


def test_gold_ner_missing_tags(en_tokenizer):
    doc = en_tokenizer("I flew to Silicon Valley via London.")
    biluo_tags = [None, "O", "O", "B-LOC", "L-LOC", "O", "U-GPE", "O"]
    gold = GoldParse(doc, entities=biluo_tags)  # noqa: F841


def test_iob_to_biluo():
    good_iob = ["O", "O", "B-LOC", "I-LOC", "O", "B-PERSON"]
    good_biluo = ["O", "O", "B-LOC", "L-LOC", "O", "U-PERSON"]
    bad_iob = ["O", "O", "\"", "B-LOC", "I-LOC"]
    converted_biluo = iob_to_biluo(good_iob)
    assert good_biluo == converted_biluo
    with pytest.raises(ValueError):
        iob_to_biluo(bad_iob)


def test_roundtrip_docs_to_json():
    text = "I flew to Silicon Valley via London."
    cats = {"TRAVEL": 1.0, "BAKING": 0.0}
    nlp = English()
    doc = nlp(text)
    doc.cats = cats
    doc[0].is_sent_start = True
    for i in range(1, len(doc)):
        doc[i].is_sent_start = False

    with make_tempdir() as tmpdir:
        json_file = tmpdir / "roundtrip.json"
        srsly.write_json(json_file, [docs_to_json(doc)])
        goldcorpus = GoldCorpus(train=str(json_file), dev=str(json_file))

    reloaded_doc, goldparse = next(goldcorpus.train_docs(nlp))

    assert len(doc) == goldcorpus.count_train()
    assert text == reloaded_doc.text
    assert "TRAVEL" in goldparse.cats
    assert "BAKING" in goldparse.cats
    assert cats["TRAVEL"] == goldparse.cats["TRAVEL"]
    assert cats["BAKING"] == goldparse.cats["BAKING"]


def test_gold_constructor():
    """Test that the GoldParse constructor works fine"""
    nlp = English()
    doc = nlp("This is a sentence")
    gold = GoldParse(doc, cats={"cat1": 1.0, "cat2": 0.0})

    assert gold.cats["cat1"]
    assert not gold.cats["cat2"]
    assert gold.words == ["This", "is", "a", "sentence"]


def test_gold_orig_annot():
    nlp = English()
    doc = nlp("This is a sentence")
    gold = GoldParse(doc, cats={"cat1": 1.0, "cat2": 0.0})

    ids, words, tags, heads, labels, iob = zip(*gold.orig_annot)
    assert words == ("This", "is", "a", "sentence")


def test_tuple_format_implicit():
    """Test tuple format with implicit GoldParse creation"""

    train_data = [
        ("Uber blew through $1 million a week", {"entities": [(0, 4, "ORG")]}),
        (
            "Spotify steps up Asia expansion",
            {"entities": [(0, 8, "ORG"), (17, 21, "LOC")]},
        ),
        ("Google rebrands its business apps", {"entities": [(0, 6, "ORG")]}),
    ]

    _train(train_data)


def test_tuple_format_implicit_invalid():
    """Test that an error is thrown fro an implicit invalid GoldParse field"""

    train_data = [
        ("Uber blew through $1 million a week", {"frumble": [(0, 4, "ORG")]}),
        (
            "Spotify steps up Asia expansion",
            {"entities": [(0, 8, "ORG"), (17, 21, "LOC")]},
        ),
        ("Google rebrands its business apps", {"entities": [(0, 6, "ORG")]}),
    ]

    with pytest.raises(ValueError):
        _train(train_data)


def _train(train_data):
    nlp = English()
    ner = nlp.create_pipe("ner")
    ner.add_label("ORG")
    ner.add_label("LOC")
    nlp.add_pipe(ner)

    optimizer = nlp.begin_training()
    for i in range(5):
        losses = {}
        batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.001))
        for batch in batches:
            texts, annotations = zip(*batch)
            nlp.update(texts, annotations, sgd=optimizer, losses=losses)
