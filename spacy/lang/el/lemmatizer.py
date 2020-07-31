from typing import Optional, List

from thinc.api import Model

from ...lookups import Lookups
from ...parts_of_speech import NAMES as UPOS_NAMES
from ...pipeline import Lemmatizer
from ...tokens import Token
from ...vocab import Vocab


class GreekLemmatizer(Lemmatizer):
    """
    Greek language lemmatizer applies the default rule based lemmatization
    procedure with some modifications for better Greek language support.

    The first modification is that it checks if the word for lemmatization is
    already a lemma and if yes, it just returns it.
    The second modification is about removing the base forms function which is
    not applicable for Greek language.
    """
    def __init__(
        self,
        vocab: Vocab,
        model: Optional[Model],
        name: str = "lemmatizer",
        *,
        mode: str = "rule",
        lookups: Optional[Lookups] = None,
    ) -> None:
        super().__init__(vocab, model, name, mode=mode, lookups=lookups)
        self.cache_features["rule"] = ["LOWER", "POS"]

    def rule_lemmatize(self, token: Token) -> List[str]:
        """Lemmatize using a rule-based approach.

        token (Token): The token to lemmatize.
        RETURNS (list): The available lemmas for the string.
        """
        string = token.text
        univ_pos = token.pos_
        if isinstance(univ_pos, int):
            univ_pos = UPOS_NAMES.get(univ_pos, "X")
        univ_pos = univ_pos.lower()
        if univ_pos in ("", "eol", "space"):
            return [string.lower()]

        index_table = self.lookups.get_table("lemma_index", {})
        exc_table = self.lookups.get_table("lemma_exc", {})
        rules_table = self.lookups.get_table("lemma_rules", {})
        index = index_table.get(univ_pos, {})
        exceptions = exc_table.get(univ_pos, {})
        rules = rules_table.get(univ_pos, {})

        string = string.lower()
        forms = []
        if string in index:
            forms.append(string)
            return forms
        forms.extend(exceptions.get(string, []))
        oov_forms = []
        if not forms:
            for old, new in rules:
                if string.endswith(old):
                    form = string[: len(string) - len(old)] + new
                    if not form:
                        pass
                    elif form in index or not form.isalpha():
                        forms.append(form)
                    else:
                        oov_forms.append(form)
        if not forms:
            forms.extend(oov_forms)
        if not forms:
            forms.append(string)
        return list(set(forms))
