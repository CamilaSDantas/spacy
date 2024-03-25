from ...symbols import ORTH
from ...util import update_exc
from ..tokenizer_exceptions import BASE_EXCEPTIONS

_exc = {}

for orth in [
    "Chr.",
    "apr.",
    "atm.",
    "aug.",
    "avgr.",
    "árg.",
    "ávís.",
    "beinl.",
    "blkv.",
    "blaðkv.",
    "blm.",
    "blaðm.",
    "blaðstj.",
    "blkv.",
    "blm.",
    "bls.",
    "blstj.",
    "blaðstj.",
    "cand.",
    "dagf.",
    "des.",
    "dkr.",
    "dr.",
    "e.Kr.",
    "eint.",
    "ex.",
    "exam.",
    "f.",
    "f.Kr.",
    "fa.",
    "fam.",
    "feb.",
    "febr.",
    "ff.",
    "fl.",
    "form.",
    "frí.",
    "fyrrv.",
    "góðk.",
    "h.m.",
    "hósd.",
    "innt.",
    "jan.",
    "kap.",
    "kgl.",
    "kl.",
    "kr.",
    "leyg.",
    "m.a.",
    "mðr.",
    "m.o.",
    "m.ø.",
    "mia.",
    "mik.",
    "min.",
    "mió.",
    "mán.",
    "mðr.",
    "nov.",
    "nr.",
    "nto.",
    "nov.",
    "nút.",
    "o.a.",
    "o.a.m.",
    "o.a.tíl.",
    "o.fl.",
    "ff.",
    "o.m.a.",
    "o.o.",
    "o.s.fr.",
    "o.tíl.",
    "o.u.",
    "o.ø.",
    "okt.",
    "omf.",
    "ph.d.",
    "phil.",
    "pr.",
    "pst.",
    "ritstj.",
    "s.",
    "sb.",
    "sbr.",
    "sbrt.",
    "sek.",
    "sep.",
    "sept.",
    "serst.",
    "smb.",
    "smbr.",
    "sms.",
    "smst.",
    "smb.",
    "sb.",
    "sbrt.",
    "sp.",
    "sept.",
    "spf.",
    "spsk.",
    "stk.",
    "sunnud.",
    "t.",
    "t.d.",
    "t.e.",
    "t.o.v.",
    "t.s.",
    "t.s.s.",
    "tlf.",
    "t.v.s",
    "t.v.s.",
    "tel.",
    "tils.",
    "tlf.",
    "tsk.",
    "t.o.v.",
    "t.d.",
    "tús.",
    "týs.",
    "uml.",
    "ums.",
    "uppl.",
    "upprfr.",
    "uppr.",
    "útg.",
    "útl.",
    "útr.",
    "vanl.",
    "upprfr.",
    "v.",
    "v.h.",
    "v.m.",
    "v.ø.o.",
    "vanl.",
    "viðm.",
    "viðv.",
    "vm.",
    "v.m.",
    "á.Kr.",
    "árg.",
    "ávís.",
    "útg.",
    "útl.",
    "útr.",
]:
    _exc[orth] = [{ORTH: orth}]
    capitalized = orth.capitalize()
    _exc[capitalized] = [{ORTH: capitalized}]

TOKENIZER_EXCEPTIONS = update_exc(BASE_EXCEPTIONS, _exc)
