"""Words like numbers are recognized correctly."""
import pytest

def test_long_text(sl_tokenizer):
    # Excerpt: European Convention on Human Rights
    text = """
Vlade podpisnice te Konvencije, članice Sveta Evrope, so se,
upoštevajoč Splošno deklaracijo o človekovih pravicah, ki
jo je razglasila Generalna Skupščina Združenih narodov dne
10. decembra 1948,
upoštevajoč, da si ta deklaracija prizadeva zagotoviti splošno in
učinkovito priznavanje in spoštovanje v njej razglašenih pravic,
upoštevajoč, da je cilj Sveta Evrope doseči večjo enotnost med
njegovimi članicami, in da je eden izmed načinov za zagotavljanje
tega cilja varstvo in nadaljnji razvoj človekovih pravic in temeljnih
svoboščin,
ponovno potrjujoč svojo globoko vero v temeljne svoboščine, na
katerih temeljita pravičnost in mir v svetu, in ki jih je mogoče najbolje
zavarovati na eni strani z dejansko politično demokracijo in na drugi
strani s skupnim razumevanjem in spoštovanjem človekovih pravic,
od katerih so te svoboščine odvisne,    
"""
    tokens = sl_tokenizer(text)
    assert len(tokens) == 153