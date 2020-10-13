# coding: utf-8
from __future__ import unicode_literals

import pytest


def test_noun_chunks_is_parsed(da_tokenizer):
    """Test that noun_chunks raises Value Error for 'da' language if Doc is not parsed.
    To check this test, we're constructing a Doc
    with a new Vocab here and forcing is_parsed to 'False'
    to make sure the noun chunks don't run.
    """
    doc = da_tokenizer("Det er en sætning")
    doc.is_parsed = False
    with pytest.raises(ValueError):
        list(doc.noun_chunks)
