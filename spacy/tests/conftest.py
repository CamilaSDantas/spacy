import pytest
from spacy.util import get_lang_class


def pytest_addoption(parser):
    parser.addoption("--slow", action="store_true", help="include slow tests")


def pytest_runtest_setup(item):
    def getopt(opt):
        # When using 'pytest --pyargs spacy' to test an installed copy of
        # spacy, pytest skips running our pytest_addoption() hook. Later, when
        # we call getoption(), pytest raises an error, because it doesn't
        # recognize the option we're asking about. To avoid this, we need to
        # pass a default value. We default to False, i.e., we act like all the
        # options weren't given.
        return item.config.getoption(f"--{opt}", False)

    for opt in ["slow"]:
        if opt in item.keywords and not getopt(opt):
            pytest.skip(f"need --{opt} option to run")


# Fixtures for language tokenizers (languages sorted alphabetically)


@pytest.fixture(scope="module")
def tokenizer():
    return get_lang_class("xx")().tokenizer


@pytest.fixture(scope="session")
def ar_tokenizer():
    return get_lang_class("ar")().tokenizer


@pytest.fixture(scope="session")
def bn_tokenizer():
    return get_lang_class("bn")().tokenizer


@pytest.fixture(scope="session")
def ca_tokenizer():
    return get_lang_class("ca")().tokenizer


@pytest.fixture(scope="session")
def da_tokenizer():
    return get_lang_class("da")().tokenizer


@pytest.fixture(scope="session")
def de_tokenizer():
    return get_lang_class("de")().tokenizer


@pytest.fixture(scope="session")
def el_tokenizer():
    return get_lang_class("el")().tokenizer


@pytest.fixture(scope="session")
def en_tokenizer():
    return get_lang_class("en")().tokenizer


@pytest.fixture(scope="session")
def en_vocab():
    return get_lang_class("en")().vocab


@pytest.fixture(scope="session")
def en_parser(en_vocab):
    nlp = get_lang_class("en")(en_vocab)
    return nlp.create_pipe("parser")


@pytest.fixture(scope="session")
def es_tokenizer():
    return get_lang_class("es")().tokenizer


@pytest.fixture(scope="session")
def eu_tokenizer():
    return get_lang_class("eu")().tokenizer


@pytest.fixture(scope="session")
def fa_tokenizer():
    return get_lang_class("fa")().tokenizer


@pytest.fixture(scope="session")
def fi_tokenizer():
    return get_lang_class("fi")().tokenizer


@pytest.fixture(scope="session")
def fr_tokenizer():
    return get_lang_class("fr")().tokenizer


@pytest.fixture(scope="session")
def ga_tokenizer():
    return get_lang_class("ga")().tokenizer


@pytest.fixture(scope="session")
def gu_tokenizer():
    return get_lang_class("gu")().tokenizer


@pytest.fixture(scope="session")
def he_tokenizer():
    return get_lang_class("he")().tokenizer


@pytest.fixture(scope="session")
def hr_tokenizer():
    return get_lang_class("hr")().tokenizer


@pytest.fixture
def hu_tokenizer():
    return get_lang_class("hu")().tokenizer


@pytest.fixture(scope="session")
def id_tokenizer():
    return get_lang_class("id")().tokenizer


@pytest.fixture(scope="session")
def it_tokenizer():
    return get_lang_class("it")().tokenizer


@pytest.fixture(scope="session")
def ja_tokenizer():
    pytest.importorskip("sudachipy")
    return get_lang_class("ja")().tokenizer


@pytest.fixture(scope="session")
def ko_tokenizer():
    pytest.importorskip("natto")
    return get_lang_class("ko")().tokenizer


@pytest.fixture(scope="session")
def lb_tokenizer():
    return get_lang_class("lb")().tokenizer


@pytest.fixture(scope="session")
def lt_tokenizer():
    return get_lang_class("lt")().tokenizer


@pytest.fixture(scope="session")
def ml_tokenizer():
    return get_lang_class("ml")().tokenizer


@pytest.fixture(scope="session")
def nb_tokenizer():
    return get_lang_class("nb")().tokenizer


@pytest.fixture(scope="session")
def ne_tokenizer():
    return get_lang_class("ne").Defaults.create_tokenizer()


@pytest.fixture(scope="session")
def nl_tokenizer():
    return get_lang_class("nl")().tokenizer


@pytest.fixture(scope="session")
def pl_tokenizer():
    return get_lang_class("pl")().tokenizer


@pytest.fixture(scope="session")
def pt_tokenizer():
    return get_lang_class("pt")().tokenizer


@pytest.fixture(scope="session")
def ro_tokenizer():
    return get_lang_class("ro")().tokenizer


@pytest.fixture(scope="session")
def ru_tokenizer():
    pytest.importorskip("pymorphy2")
    return get_lang_class("ru")().tokenizer


@pytest.fixture
def ru_lemmatizer():
    pytest.importorskip("pymorphy2")
    return get_lang_class("ru")().vocab.morphology.lemmatizer


@pytest.fixture(scope="session")
def sr_tokenizer():
    return get_lang_class("sr")().tokenizer


@pytest.fixture(scope="session")
def sv_tokenizer():
    return get_lang_class("sv")().tokenizer


@pytest.fixture(scope="session")
def th_tokenizer():
    pytest.importorskip("pythainlp")
    return get_lang_class("th")().tokenizer


@pytest.fixture(scope="session")
def tr_tokenizer():
    return get_lang_class("tr")().tokenizer


@pytest.fixture(scope="session")
def tt_tokenizer():
    return get_lang_class("tt")().tokenizer


@pytest.fixture(scope="session")
def uk_tokenizer():
    pytest.importorskip("pymorphy2")
    pytest.importorskip("pymorphy2.lang")
    return get_lang_class("uk")().tokenizer


@pytest.fixture(scope="session")
def ur_tokenizer():
    return get_lang_class("ur")().tokenizer


@pytest.fixture(scope="session")
def yo_tokenizer():
    return get_lang_class("yo")().tokenizer


@pytest.fixture(scope="session")
def zh_tokenizer_char():
    nlp = get_lang_class("zh")()
    return nlp.tokenizer


@pytest.fixture(scope="session")
def zh_tokenizer_jieba():
    pytest.importorskip("jieba")
    config = {
        "@tokenizers": "spacy.ChineseTokenizer.v1",
        "segmenter": "jieba",
    }
    nlp = get_lang_class("zh").from_config({"nlp": {"tokenizer": config}})
    return nlp.tokenizer


@pytest.fixture(scope="session")
def zh_tokenizer_pkuseg():
    pytest.importorskip("pkuseg")
    config = {
        "@tokenizers": "spacy.ChineseTokenizer.v1",
        "segmenter": "pkuseg",
        "pkuseg_model": "default",
    }
    nlp = get_lang_class("zh").from_config({"nlp": {"tokenizer": config}})
    return nlp.tokenizer


@pytest.fixture(scope="session")
def hy_tokenizer():
    return get_lang_class("hy")().tokenizer
