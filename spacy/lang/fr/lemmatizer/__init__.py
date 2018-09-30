# coding: utf8
from __future__ import unicode_literals

from .lookup import LOOKUP
from ._adjectives import ADJECTIVES
from ._adjectives_irreg import ADJECTIVES_IRREG
from ._adverbs import ADVERBS
from ._nouns import NOUNS
from ._nouns_irreg import NOUNS_IRREG
from ._lemma_rules import ADJECTIVE_RULES, NOUN_RULES


LEMMA_INDEX = {'adj': ADJECTIVES, 'adv': ADVERBS, 'noun': NOUNS}

LEMMA_EXC = {'adj': ADJECTIVES_IRREG, 'noun': NOUNS_IRREG}

LEMMA_RULES = {'adj': ADJECTIVE_RULES, 'noun': NOUN_RULES}
