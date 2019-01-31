# coding: utf8
from __future__ import unicode_literals

from .char_classes import LIST_PUNCT, LIST_ELLIPSES, LIST_QUOTES, LIST_CURRENCY, LIST_ICONS
from .char_classes import HYPHENS
from .char_classes import CURRENCY, UNITS
from .char_classes import CONCAT_QUOTES, ALPHA_LOWER, ALPHA_UPPER, ALPHA


_prefixes = (
    ["§", "%", "=", r"\+(?![0-9])"]
    + LIST_PUNCT
    + LIST_ELLIPSES
    + LIST_QUOTES
    + LIST_CURRENCY
    + LIST_ICONS
)


_suffixes = (
    LIST_PUNCT
    + LIST_ELLIPSES
    + LIST_QUOTES
    + LIST_ICONS
    + ["'s", "'S", "’s", "’S"]
    + [
        r"(?<=[0-9])\+",
        r"(?<=°[FfCcKk])\.",
        r"(?<=[0-9])(?:{c})".format(c=CURRENCY),
        r"(?<=[0-9])(?:{u})".format(u=UNITS),
        r"(?<=[0-9{al}{e}(?:{q})])\.".format(al=ALPHA_LOWER, e=r"%²\-\+", q=CONCAT_QUOTES),
        r"(?<=[{a}][{a}])\.".format(a=ALPHA_UPPER),
    ]
)

_infixes = (
    LIST_ELLIPSES
    + LIST_ICONS
    + [
        r"(?<=[0-9])[+\-\*^](?=[0-9-])",
        r"(?<=[{al}])\.(?=[{au}])".format(al=ALPHA_LOWER, au=ALPHA_UPPER),
        r"(?<=[{a}]),(?=[{a}])".format(a=ALPHA),
        r'(?<=[{a}])(?:{h})(?=[{a}])'.format(a=ALPHA, h=HYPHENS),
        r'(?<=[{a}])[:<>=/](?=[{a}])'.format(a=ALPHA),
    ]
)

TOKENIZER_PREFIXES = _prefixes
TOKENIZER_SUFFIXES = _suffixes
TOKENIZER_INFIXES = _infixes
