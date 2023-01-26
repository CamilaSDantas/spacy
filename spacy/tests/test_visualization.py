import pytest
from wasabi.util import supports_ansi
from spacy.visualization import AttributeFormat, render_dep_tree, render_table
from spacy.tokens import Span, Doc, Token


SUPPORTS_ANSI = supports_ansi()


@pytest.fixture
def horse_doc(en_vocab):
    return Doc(
        en_vocab,
        words=[
            "I",
            "saw",
            "a",
            "horse",
            "yesterday",
            "that",
            "was",
            "injured",
            ".",
        ],
        heads=[1, None, 3, 1, 1, 7, 7, 3, 1],
        deps=["dep"] * 9,
    )


def test_viz_dep_tree_basic(en_vocab):
    """Test basic dependency tree display."""
    doc = Doc(
        en_vocab,
        words=[
            "The",
            "big",
            "dog",
            "chased",
            "the",
            "frightened",
            "cat",
            "mercilessly",
            ".",
        ],
        heads=[2, 2, 3, None, 6, 6, 3, 3, 3],
        deps=["dep"] * 9,
    )
    dep_tree = render_dep_tree(doc[0 : len(doc)], True)
    assert dep_tree == [
        "<╗  ",
        "<╣  ",
        "═╝<╗",
        "═══╣",
        "<╗ ║",
        "<╣ ║",
        "═╝<╣",
        "<══╣",
        "<══╝",
    ]
    dep_tree = render_dep_tree(doc[0 : len(doc)], False)
    assert dep_tree == [
        "  ╔>",
        "  ╠>",
        "╔>╚═",
        "╠═══",
        "║ ╔>",
        "║ ╠>",
        "╠>╚═",
        "╠══>",
        "╚══>",
    ]


def test_viz_dep_tree_non_initial_sent(en_vocab):
    """Test basic dependency tree display."""
    doc = Doc(
        en_vocab,
        words=[
            "Something",
            "happened",
            ".",
            "The",
            "big",
            "dog",
            "chased",
            "the",
            "frightened",
            "cat",
            "mercilessly",
            ".",
        ],
        heads=[0, None, 0, 5, 5, 6, None, 9, 9, 6, 6, 6],
        deps=["dep"] * 12,
    )
    dep_tree = render_dep_tree(doc[3 : len(doc)], True)
    assert dep_tree == [
        "<╗  ",
        "<╣  ",
        "═╝<╗",
        "═══╣",
        "<╗ ║",
        "<╣ ║",
        "═╝<╣",
        "<══╣",
        "<══╝",
    ]
    dep_tree = render_dep_tree(doc[3 : len(doc)], False)
    assert dep_tree == [
        "  ╔>",
        "  ╠>",
        "╔>╚═",
        "╠═══",
        "║ ╔>",
        "║ ╠>",
        "╠>╚═",
        "╠══>",
        "╚══>",
    ]


def test_viz_dep_tree_non_projective(horse_doc):
    """Test dependency tree display with a non-projective dependency."""
    dep_tree = render_dep_tree(horse_doc[0 : len(horse_doc)], True)
    assert dep_tree == [
        "<╗    ",
        "═╩═══╗",
        "<╗   ║",
        "═╩═╗<╣",
        "<══║═╣",
        "<╗ ║ ║",
        "<╣ ║ ║",
        "═╝<╝ ║",
        "<════╝",
    ]
    dep_tree = render_dep_tree(horse_doc[0 : len(horse_doc)], False)
    assert dep_tree == [
        "    ╔>",
        "╔═══╩═",
        "║   ╔>",
        "╠>╔═╩═",
        "╠═║══>",
        "║ ║ ╔>",
        "║ ║ ╠>",
        "║ ╚>╚═",
        "╚════>",
    ]


def test_viz_dep_tree_highly_nonprojective(pl_vocab):
    """Test a highly non-projective tree (colloquial Polish)."""
    doc = Doc(
        pl_vocab,
        words=[
            "Owczarki",
            "przecież",
            "niemieckie",
            "zawsze",
            "wierne",
            "są",
            "bardzo",
            ".",
        ],
        heads=[5, 5, 0, 5, 5, None, 4, 5],
        deps=["dep"] * 8,
    )
    dep_tree = render_dep_tree(doc[0 : len(doc)], True)
    assert dep_tree == [
        "═╗<╗",
        " ║<╣",
        "<╝ ║",
        "<══╣",
        "═╗<╣",
        "═══╣",
        "<╝ ║",
        "<══╝",
    ]
    dep_tree = render_dep_tree(doc[0 : len(doc)], False)
    assert dep_tree == [
        "╔>╔═",
        "╠>║ ",
        "║ ╚>",
        "╠══>",
        "╠>╔═",
        "╠═══",
        "║ ╚>",
        "╚══>",
    ]


def test_viz_dep_tree_input_not_span(horse_doc):
    """Test dependency tree display behaviour when the input is not a Span."""
    with pytest.raises(ValueError):
        render_dep_tree(horse_doc[1:3], True)


def test_viz_render_native_attributes(horse_doc):
    assert AttributeFormat("head.i").render(horse_doc[2]) == "3"
    assert AttributeFormat("head.i").render(horse_doc[2], right_pad_to_len=3) == "3  "
    assert AttributeFormat("dep_").render(horse_doc[2]) == "dep"
    with pytest.raises(AttributeError):
        AttributeFormat("depp").render(horse_doc[2])
    with pytest.raises(AttributeError):
        AttributeFormat("tree_left").render(horse_doc[2])
    with pytest.raises(AttributeError):
        AttributeFormat("tree_right").render(horse_doc[2])


def test_viz_render_colors(horse_doc):
    assert (
        AttributeFormat(
            "dep_",
            value_dep_fg_colors={"dep": 2},
            value_dep_bg_colors={"dep": 11},
        ).render(horse_doc[2])
        == "\x1b[38;5;2;48;5;11mdep\x1b[0m"
        if SUPPORTS_ANSI
        else "dep"
    )

    # foreground only
    assert (
        AttributeFormat(
            "dep_",
            value_dep_fg_colors={"dep": 2},
        ).render(horse_doc[2])
        == "\x1b[38;5;2mdep\x1b[0m"
        if SUPPORTS_ANSI
        else "dep"
    )

    # background only
    assert (
        AttributeFormat(
            "dep_",
            value_dep_bg_colors={"dep": 11},
        ).render(horse_doc[2])
        == "\x1b[48;5;11mdep\x1b[0m"
        if SUPPORTS_ANSI
        else "dep"
    )


def test_viz_render_custom_attributes(horse_doc):
    Token.set_extension("test", default="tested1", force=True)
    assert AttributeFormat("_.test").render(horse_doc[2]) == "tested1"

    class Test:
        def __init__(self):
            self.inner_test = "tested2"

    Token.set_extension("test", default=Test(), force=True)
    assert AttributeFormat("_.test.inner_test").render(horse_doc[2]) == "tested2"

    with pytest.raises(AttributeError):
        AttributeFormat("._depp").render(horse_doc[2])


def test_viz_minimal_render_table_one_sentence(
    fully_featured_doc_one_sentence,
):
    formats = [
        AttributeFormat("tree_left"),
        AttributeFormat("dep_"),
        AttributeFormat("text"),
        AttributeFormat("lemma_"),
        AttributeFormat("pos_"),
        AttributeFormat("tag_"),
        AttributeFormat("morph"),
        AttributeFormat("ent_type_"),
    ]
    assert (
        render_table(fully_featured_doc_one_sentence, formats, spacing=3).strip()
        == """
  ╔>╔═   poss       Sarah     sarah     PROPN   NNP   NounType=prop|Number=sing   PERSON
  ║ ╚>   case       's        's        PART    POS   Poss=yes                          
╔>╚═══   nsubj      sister    sister    NOUN    NN    Number=sing                       
╠═════   ROOT       flew      fly       VERB    VBD   Tense=past|VerbForm=fin           
╠>╔═══   prep       to        to        ADP     IN                                      
║ ║ ╔>   compound   Silicon   silicon   PROPN   NNP   NounType=prop|Number=sing   GPE   
║ ╚>╚═   pobj       Valley    valley    PROPN   NNP   NounType=prop|Number=sing   GPE   
╠══>╔═   prep       via       via       ADP     IN                                      
║   ╚>   pobj       London    london    PROPN   NNP   NounType=prop|Number=sing   GPE   
╚════>   punct      .         .         PUNCT   .     PunctType=peri
    """.strip()
    )


def test_viz_minimal_render_table_empty_text(
    en_vocab,
):
    # no headers
    formats = [
        AttributeFormat("tree_left"),
        AttributeFormat("dep_"),
        AttributeFormat("text"),
        AttributeFormat("lemma_"),
        AttributeFormat("pos_"),
        AttributeFormat("tag_"),
        AttributeFormat("morph"),
        AttributeFormat("ent_type_"),
    ]
    assert render_table(Doc(en_vocab), formats, spacing=3).strip() == ""

    # headers
    formats = [
        AttributeFormat("tree_left", name="tree"),
        AttributeFormat("dep_"),
        AttributeFormat("text"),
        AttributeFormat("lemma_"),
        AttributeFormat("pos_"),
        AttributeFormat("tag_"),
        AttributeFormat("morph"),
        AttributeFormat("ent_type_", name="ent"),
    ]
    assert render_table(Doc(en_vocab), formats, spacing=3).strip() == ""


def test_viz_minimal_render_table_spacing(
    fully_featured_doc_one_sentence,
):
    formats = [
        AttributeFormat("tree_left"),
        AttributeFormat("dep_"),
        AttributeFormat("text"),
        AttributeFormat("lemma_"),
        AttributeFormat("pos_"),
        AttributeFormat("tag_"),
        AttributeFormat("morph"),
        AttributeFormat("ent_type_"),
    ]
    assert (
        render_table(fully_featured_doc_one_sentence, formats, spacing=1).strip()
        == """
  ╔>╔═ poss     Sarah   sarah   PROPN NNP NounType=prop|Number=sing PERSON
  ║ ╚> case     's      's      PART  POS Poss=yes                        
╔>╚═══ nsubj    sister  sister  NOUN  NN  Number=sing                     
╠═════ ROOT     flew    fly     VERB  VBD Tense=past|VerbForm=fin         
╠>╔═══ prep     to      to      ADP   IN                                  
║ ║ ╔> compound Silicon silicon PROPN NNP NounType=prop|Number=sing GPE   
║ ╚>╚═ pobj     Valley  valley  PROPN NNP NounType=prop|Number=sing GPE   
╠══>╔═ prep     via     via     ADP   IN                                  
║   ╚> pobj     London  london  PROPN NNP NounType=prop|Number=sing GPE   
╚════> punct    .       .       PUNCT .   PunctType=peri
    """.strip()
    )


def test_viz_minimal_render_table_two_sentences(
    fully_featured_doc_two_sentences,
):
    formats = [
        AttributeFormat("tree_left"),
        AttributeFormat("dep_"),
        AttributeFormat("text"),
        AttributeFormat("lemma_"),
        AttributeFormat("pos_"),
        AttributeFormat("tag_"),
        AttributeFormat("morph"),
        AttributeFormat("ent_type_"),
    ]

    assert (
        render_table(fully_featured_doc_two_sentences, formats, spacing=3).strip()
        == """
  ╔>╔═   poss       Sarah     sarah     PROPN   NNP   NounType=prop|Number=sing   PERSON
  ║ ╚>   case       's        's        PART    POS   Poss=yes                          
╔>╚═══   nsubj      sister    sister    NOUN    NN    Number=sing                       
╠═════   ROOT       flew      fly       VERB    VBD   Tense=past|VerbForm=fin           
╠>╔═══   prep       to        to        ADP     IN                                      
║ ║ ╔>   compound   Silicon   silicon   PROPN   NNP   NounType=prop|Number=sing   GPE   
║ ╚>╚═   pobj       Valley    valley    PROPN   NNP   NounType=prop|Number=sing   GPE   
╠══>╔═   prep       via       via       ADP     IN                                      
║   ╚>   pobj       London    london    PROPN   NNP   NounType=prop|Number=sing   GPE   
╚════>   punct      .         .         PUNCT   .     PunctType=peri                    


╔>   nsubj   She     she    PRON    PRP   Case=Nom|Gender=Fem|Number=Sing|Person=3|PronType=Prs    
╠═   ROOT    loved   love   VERB    VBD   Tense=Past|VerbForm=Fin                                  
╠>   dobj    it      it     PRON    PRP   Case=Acc|Gender=Neut|Number=Sing|Person=3|PronType=Prs   
╚>   punct   .       .      PUNCT   .     PunctType=peri    
""".strip()
    )


def test_viz_rich_render_table_one_sentence(
    fully_featured_doc_one_sentence,
):
    formats = [
        AttributeFormat("tree_left", name="tree", aligns="r", fg_color=2),
        AttributeFormat("dep_", name="dep", fg_color=2),
        AttributeFormat("i", name="index", aligns="r"),
        AttributeFormat("text", name="text"),
        AttributeFormat("lemma_", name="lemma"),
        AttributeFormat("pos_", name="pos", fg_color=100),
        AttributeFormat("tag_", name="tag", fg_color=100),
        AttributeFormat("morph", name="morph", fg_color=100, max_width=15),
        AttributeFormat(
            "ent_type_",
            name="ent",
            fg_color=196,
            value_dep_fg_colors={"PERSON": 50},
            value_dep_bg_colors={"PERSON": 12},
        ),
    ]
    assert (
        render_table(fully_featured_doc_one_sentence, formats, spacing=3)
        == "\n\x1b[38;5;2m  tree\x1b[0m   \x1b[38;5;2mdep     \x1b[0m   index   text      lemma     \x1b[38;5;100mpos  \x1b[0m   \x1b[38;5;100mtag\x1b[0m   \x1b[38;5;100mmorph          \x1b[0m   \x1b[38;5;196ment   \x1b[0m\n\x1b[38;5;2m------\x1b[0m   \x1b[38;5;2m--------\x1b[0m   -----   -------   -------   \x1b[38;5;100m-----\x1b[0m   \x1b[38;5;100m---\x1b[0m   \x1b[38;5;100m---------------\x1b[0m   \x1b[38;5;196m------\x1b[0m\n\x1b[38;5;2m  ╔>╔═\x1b[0m   \x1b[38;5;2mposs    \x1b[0m   0       Sarah     sarah     \x1b[38;5;100mPROPN\x1b[0m   \x1b[38;5;100mNNP\x1b[0m   \x1b[38;5;100mNounType=prop|N\x1b[0m   \x1b[38;5;196m\x1b[38;5;50;48;5;12mPERSON\x1b[0m\x1b[0m\n\x1b[38;5;2m  ║ ╚>\x1b[0m   \x1b[38;5;2mcase    \x1b[0m   1       's        's        \x1b[38;5;100mPART \x1b[0m   \x1b[38;5;100mPOS\x1b[0m   \x1b[38;5;100mPoss=yes       \x1b[0m   \x1b[38;5;196m      \x1b[0m\n\x1b[38;5;2m╔>╚═══\x1b[0m   \x1b[38;5;2mnsubj   \x1b[0m   2       sister    sister    \x1b[38;5;100mNOUN \x1b[0m   \x1b[38;5;100mNN \x1b[0m   \x1b[38;5;100mNumber=sing    \x1b[0m   \x1b[38;5;196m      \x1b[0m\n\x1b[38;5;2m╠═════\x1b[0m   \x1b[38;5;2mROOT    \x1b[0m   3       flew      fly       \x1b[38;5;100mVERB \x1b[0m   \x1b[38;5;100mVBD\x1b[0m   \x1b[38;5;100mTense=past|Verb\x1b[0m   \x1b[38;5;196m      \x1b[0m\n\x1b[38;5;2m╠>╔═══\x1b[0m   \x1b[38;5;2mprep    \x1b[0m   4       to        to        \x1b[38;5;100mADP  \x1b[0m   \x1b[38;5;100mIN \x1b[0m   \x1b[38;5;100m               \x1b[0m   \x1b[38;5;196m      \x1b[0m\n\x1b[38;5;2m║ ║ ╔>\x1b[0m   \x1b[38;5;2mcompound\x1b[0m   5       Silicon   silicon   \x1b[38;5;100mPROPN\x1b[0m   \x1b[38;5;100mNNP\x1b[0m   \x1b[38;5;100mNounType=prop|N\x1b[0m   \x1b[38;5;196mGPE   \x1b[0m\n\x1b[38;5;2m║ ╚>╚═\x1b[0m   \x1b[38;5;2mpobj    \x1b[0m   6       Valley    valley    \x1b[38;5;100mPROPN\x1b[0m   \x1b[38;5;100mNNP\x1b[0m   \x1b[38;5;100mNounType=prop|N\x1b[0m   \x1b[38;5;196mGPE   \x1b[0m\n\x1b[38;5;2m╠══>╔═\x1b[0m   \x1b[38;5;2mprep    \x1b[0m   7       via       via       \x1b[38;5;100mADP  \x1b[0m   \x1b[38;5;100mIN \x1b[0m   \x1b[38;5;100m               \x1b[0m   \x1b[38;5;196m      \x1b[0m\n\x1b[38;5;2m║   ╚>\x1b[0m   \x1b[38;5;2mpobj    \x1b[0m   8       London    london    \x1b[38;5;100mPROPN\x1b[0m   \x1b[38;5;100mNNP\x1b[0m   \x1b[38;5;100mNounType=prop|N\x1b[0m   \x1b[38;5;196mGPE   \x1b[0m\n\x1b[38;5;2m╚════>\x1b[0m   \x1b[38;5;2mpunct   \x1b[0m   9       .         .         \x1b[38;5;100mPUNCT\x1b[0m   \x1b[38;5;100m.  \x1b[0m   \x1b[38;5;100mPunctType=peri \x1b[0m   \x1b[38;5;196m      \x1b[0m\n\n"
        if SUPPORTS_ANSI
        else "\n\x1b[38;5;2m  tree\x1b[0m   \x1b[38;5;2mdep     \x1b[0m   index   text      lemma     pos     tag   morph             ent   \n\x1b[38;5;2m------\x1b[0m   \x1b[38;5;2m--------\x1b[0m   -----   -------   -------   -----   ---   ---------------   ------\n\x1b[38;5;2m  ╔>╔═\x1b[0m   \x1b[38;5;2mposs    \x1b[0m   0       Sarah     sarah     PROPN   NNP   NounType=prop|N   PERSON\n\x1b[38;5;2m  ║ ╚>\x1b[0m   \x1b[38;5;2mcase    \x1b[0m   1       's        's        PART    POS   Poss=yes                \n\x1b[38;5;2m╔>╚═══\x1b[0m   \x1b[38;5;2mnsubj   \x1b[0m   2       sister    sister    NOUN    NN    Number=sing             \n\x1b[38;5;2m╠═════\x1b[0m   \x1b[38;5;2mROOT    \x1b[0m   3       flew      fly       VERB    VBD   Tense=past|Verb         \n\x1b[38;5;2m╠>╔═══\x1b[0m   \x1b[38;5;2mprep    \x1b[0m   4       to        to        ADP     IN                            \n\x1b[38;5;2m║ ║ ╔>\x1b[0m   \x1b[38;5;2mcompound\x1b[0m   5       Silicon   silicon   PROPN   NNP   NounType=prop|N   GPE   \n\x1b[38;5;2m║ ╚>╚═\x1b[0m   \x1b[38;5;2mpobj    \x1b[0m   6       Valley    valley    PROPN   NNP   NounType=prop|N   GPE   \n\x1b[38;5;2m╠══>╔═\x1b[0m   \x1b[38;5;2mprep    \x1b[0m   7       via       via       ADP     IN                            \n\x1b[38;5;2m║   ╚>\x1b[0m   \x1b[38;5;2mpobj    \x1b[0m   8       London    london    PROPN   NNP   NounType=prop|N   GPE   \n\x1b[38;5;2m╚════>\x1b[0m   \x1b[38;5;2mpunct   \x1b[0m   9       .         .         PUNCT   .     PunctType=peri          \n\n"
    )

    # trigger value for value_dep shorter than maximum length in column
    formats = [
        AttributeFormat("tree_left", name="tree", aligns="r", fg_color=2),
        AttributeFormat("dep_", name="dep", fg_color=2),
        AttributeFormat("i", name="index", aligns="r"),
        AttributeFormat(
            "text",
            name="text",
            fg_color=196,
            value_dep_fg_colors={"'s": 50},
            value_dep_bg_colors={"'s": 12},
        ),
        AttributeFormat("lemma_", name="lemma"),
        AttributeFormat("pos_", name="pos", fg_color=100),
        AttributeFormat("tag_", name="tag", fg_color=100),
        AttributeFormat("morph", name="morph", fg_color=100, max_width=15),
        AttributeFormat(
            "ent_type_",
            name="ent",
        ),
    ]
    assert (
        render_table(fully_featured_doc_one_sentence, formats, spacing=3)
        == "\n\x1b[38;5;2m  tree\x1b[0m   \x1b[38;5;2mdep     \x1b[0m   index   \x1b[38;5;196mtext   \x1b[0m   lemma     \x1b[38;5;100mpos  \x1b[0m   \x1b[38;5;100mtag\x1b[0m   \x1b[38;5;100mmorph          \x1b[0m   ent   \n\x1b[38;5;2m------\x1b[0m   \x1b[38;5;2m--------\x1b[0m   -----   \x1b[38;5;196m-------\x1b[0m   -------   \x1b[38;5;100m-----\x1b[0m   \x1b[38;5;100m---\x1b[0m   \x1b[38;5;100m---------------\x1b[0m   ------\n\x1b[38;5;2m  ╔>╔═\x1b[0m   \x1b[38;5;2mposs    \x1b[0m   0       \x1b[38;5;196mSarah  \x1b[0m   sarah     \x1b[38;5;100mPROPN\x1b[0m   \x1b[38;5;100mNNP\x1b[0m   \x1b[38;5;100mNounType=prop|N\x1b[0m   PERSON\n\x1b[38;5;2m  ║ ╚>\x1b[0m   \x1b[38;5;2mcase    \x1b[0m   1       \x1b[38;5;196m\x1b[38;5;50;48;5;12m's\x1b[0m     \x1b[0m   's        \x1b[38;5;100mPART \x1b[0m   \x1b[38;5;100mPOS\x1b[0m   \x1b[38;5;100mPoss=yes       \x1b[0m         \n\x1b[38;5;2m╔>╚═══\x1b[0m   \x1b[38;5;2mnsubj   \x1b[0m   2       \x1b[38;5;196msister \x1b[0m   sister    \x1b[38;5;100mNOUN \x1b[0m   \x1b[38;5;100mNN \x1b[0m   \x1b[38;5;100mNumber=sing    \x1b[0m         \n\x1b[38;5;2m╠═════\x1b[0m   \x1b[38;5;2mROOT    \x1b[0m   3       \x1b[38;5;196mflew   \x1b[0m   fly       \x1b[38;5;100mVERB \x1b[0m   \x1b[38;5;100mVBD\x1b[0m   \x1b[38;5;100mTense=past|Verb\x1b[0m         \n\x1b[38;5;2m╠>╔═══\x1b[0m   \x1b[38;5;2mprep    \x1b[0m   4       \x1b[38;5;196mto     \x1b[0m   to        \x1b[38;5;100mADP  \x1b[0m   \x1b[38;5;100mIN \x1b[0m   \x1b[38;5;100m               \x1b[0m         \n\x1b[38;5;2m║ ║ ╔>\x1b[0m   \x1b[38;5;2mcompound\x1b[0m   5       \x1b[38;5;196mSilicon\x1b[0m   silicon   \x1b[38;5;100mPROPN\x1b[0m   \x1b[38;5;100mNNP\x1b[0m   \x1b[38;5;100mNounType=prop|N\x1b[0m   GPE   \n\x1b[38;5;2m║ ╚>╚═\x1b[0m   \x1b[38;5;2mpobj    \x1b[0m   6       \x1b[38;5;196mValley \x1b[0m   valley    \x1b[38;5;100mPROPN\x1b[0m   \x1b[38;5;100mNNP\x1b[0m   \x1b[38;5;100mNounType=prop|N\x1b[0m   GPE   \n\x1b[38;5;2m╠══>╔═\x1b[0m   \x1b[38;5;2mprep    \x1b[0m   7       \x1b[38;5;196mvia    \x1b[0m   via       \x1b[38;5;100mADP  \x1b[0m   \x1b[38;5;100mIN \x1b[0m   \x1b[38;5;100m               \x1b[0m         \n\x1b[38;5;2m║   ╚>\x1b[0m   \x1b[38;5;2mpobj    \x1b[0m   8       \x1b[38;5;196mLondon \x1b[0m   london    \x1b[38;5;100mPROPN\x1b[0m   \x1b[38;5;100mNNP\x1b[0m   \x1b[38;5;100mNounType=prop|N\x1b[0m   GPE   \n\x1b[38;5;2m╚════>\x1b[0m   \x1b[38;5;2mpunct   \x1b[0m   9       \x1b[38;5;196m.      \x1b[0m   .         \x1b[38;5;100mPUNCT\x1b[0m   \x1b[38;5;100m.  \x1b[0m   \x1b[38;5;100mPunctType=peri \x1b[0m         \n\n"
        if SUPPORTS_ANSI
        else "\n\x1b[38;5;2m  tree\x1b[0m   \x1b[38;5;2mdep     \x1b[0m   index   text      lemma     pos     tag   \x1b[38;5;100mmorph                    \x1b[0m   ent   \n\x1b[38;5;2m------\x1b[0m   \x1b[38;5;2m--------\x1b[0m   -----   -------   -------   -----   ---   \x1b[38;5;100m-------------------------\x1b[0m   ------\n\x1b[38;5;2m  ╔>╔═\x1b[0m   \x1b[38;5;2mposs    \x1b[0m   0       Sarah     sarah     PROPN   NNP   \x1b[38;5;100mNounType=prop|Number=sing\x1b[0m   PERSON\n\x1b[38;5;2m  ║ ╚>\x1b[0m   \x1b[38;5;2mcase    \x1b[0m   1       's        's        PART    POS   \x1b[38;5;100mPoss=yes                 \x1b[0m         \n\x1b[38;5;2m╔>╚═══\x1b[0m   \x1b[38;5;2mnsubj   \x1b[0m   2       sister    sister    NOUN    NN    \x1b[38;5;100mNumber=sing              \x1b[0m         \n\x1b[38;5;2m╠═════\x1b[0m   \x1b[38;5;2mROOT    \x1b[0m   3       flew      fly       VERB    VBD   \x1b[38;5;100mTense=past|VerbForm=fin  \x1b[0m         \n\x1b[38;5;2m╠>╔═══\x1b[0m   \x1b[38;5;2mprep    \x1b[0m   4       to        to        ADP     IN    \x1b[38;5;100m                         \x1b[0m         \n\x1b[38;5;2m║ ║ ╔>\x1b[0m   \x1b[38;5;2mcompound\x1b[0m   5       Silicon   silicon   PROPN   NNP   \x1b[38;5;100mNounType=prop|Number=sing\x1b[0m   GPE   \n\x1b[38;5;2m║ ╚>╚═\x1b[0m   \x1b[38;5;2mpobj    \x1b[0m   6       Valley    valley    PROPN   NNP   \x1b[38;5;100mNounType=prop|Number=sing\x1b[0m   GPE   \n\x1b[38;5;2m╠══>╔═\x1b[0m   \x1b[38;5;2mprep    \x1b[0m   7       via       via       ADP     IN    \x1b[38;5;100m                         \x1b[0m         \n\x1b[38;5;2m║   ╚>\x1b[0m   \x1b[38;5;2mpobj    \x1b[0m   8       London    london    PROPN   NNP   \x1b[38;5;100mNounType=prop|Number=sing\x1b[0m   GPE   \n\x1b[38;5;2m╚════>\x1b[0m   \x1b[38;5;2mpunct   \x1b[0m   9       .         .         PUNCT   .     \x1b[38;5;100mPunctType=peri           \x1b[0m         \n\n"
    )


def test_viz_rich_render_table_two_sentences(
    fully_featured_doc_two_sentences,
):
    formats = [
        AttributeFormat("tree_left", name="tree", aligns="r", fg_color=2),
        AttributeFormat("dep_", name="dep", fg_color=2),
        AttributeFormat("i", name="index", aligns="r"),
        AttributeFormat("text", name="text"),
        AttributeFormat("lemma_", name="lemma"),
        AttributeFormat("pos_", name="pos", fg_color=100),
        AttributeFormat("tag_", name="tag", fg_color=100),
        AttributeFormat("morph", name="morph", fg_color=100, max_width=15),
        AttributeFormat(
            "ent_type_",
            name="ent",
            fg_color=196,
            value_dep_fg_colors={"PERSON": 50},
            value_dep_bg_colors={"PERSON": 12},
        ),
    ]
    print(render_table(fully_featured_doc_two_sentences, formats, spacing=3))
    print(repr(render_table(fully_featured_doc_two_sentences, formats, spacing=3)))
    target = (
        "\n\x1b[38;5;2m  tree\x1b[0m   \x1b[38;5;2mdep     \x1b[0m   index   text      lemma     \x1b[38;5;100mpos  \x1b[0m   \x1b[38;5;100mtag\x1b[0m   \x1b[38;5;100mmorph          \x1b[0m   \x1b[38;5;196ment   \x1b[0m\n\x1b[38;5;2m------\x1b[0m   \x1b[38;5;2m--------\x1b[0m   -----   -------   -------   \x1b[38;5;100m-----\x1b[0m   \x1b[38;5;100m---\x1b[0m   \x1b[38;5;100m---------------\x1b[0m   \x1b[38;5;196m------\x1b[0m\n\x1b[38;5;2m  ╔>╔═\x1b[0m   \x1b[38;5;2mposs    \x1b[0m   0       Sarah     sarah     \x1b[38;5;100mPROPN\x1b[0m   \x1b[38;5;100mNNP\x1b[0m   \x1b[38;5;100mNounType=prop|N\x1b[0m   \x1b[38;5;196m\x1b[38;5;50;48;5;12mPERSON\x1b[0m\x1b[0m\n\x1b[38;5;2m  ║ ╚>\x1b[0m   \x1b[38;5;2mcase    \x1b[0m   1       's        's        \x1b[38;5;100mPART \x1b[0m   \x1b[38;5;100mPOS\x1b[0m   \x1b[38;5;100mPoss=yes       \x1b[0m   \x1b[38;5;196m      \x1b[0m\n\x1b[38;5;2m╔>╚═══\x1b[0m   \x1b[38;5;2mnsubj   \x1b[0m   2       sister    sister    \x1b[38;5;100mNOUN \x1b[0m   \x1b[38;5;100mNN \x1b[0m   \x1b[38;5;100mNumber=sing    \x1b[0m   \x1b[38;5;196m      \x1b[0m\n\x1b[38;5;2m╠═════\x1b[0m   \x1b[38;5;2mROOT    \x1b[0m   3       flew      fly       \x1b[38;5;100mVERB \x1b[0m   \x1b[38;5;100mVBD\x1b[0m   \x1b[38;5;100mTense=past|Verb\x1b[0m   \x1b[38;5;196m      \x1b[0m\n\x1b[38;5;2m╠>╔═══\x1b[0m   \x1b[38;5;2mprep    \x1b[0m   4       to        to        \x1b[38;5;100mADP  \x1b[0m   \x1b[38;5;100mIN \x1b[0m   \x1b[38;5;100m               \x1b[0m   \x1b[38;5;196m      \x1b[0m\n\x1b[38;5;2m║ ║ ╔>\x1b[0m   \x1b[38;5;2mcompound\x1b[0m   5       Silicon   silicon   \x1b[38;5;100mPROPN\x1b[0m   \x1b[38;5;100mNNP\x1b[0m   \x1b[38;5;100mNounType=prop|N\x1b[0m   \x1b[38;5;196mGPE   \x1b[0m\n\x1b[38;5;2m║ ╚>╚═\x1b[0m   \x1b[38;5;2mpobj    \x1b[0m   6       Valley    valley    \x1b[38;5;100mPROPN\x1b[0m   \x1b[38;5;100mNNP\x1b[0m   \x1b[38;5;100mNounType=prop|N\x1b[0m   \x1b[38;5;196mGPE   \x1b[0m\n\x1b[38;5;2m╠══>╔═\x1b[0m   \x1b[38;5;2mprep    \x1b[0m   7       via       via       \x1b[38;5;100mADP  \x1b[0m   \x1b[38;5;100mIN \x1b[0m   \x1b[38;5;100m               \x1b[0m   \x1b[38;5;196m      \x1b[0m\n\x1b[38;5;2m║   ╚>\x1b[0m   \x1b[38;5;2mpobj    \x1b[0m   8       London    london    \x1b[38;5;100mPROPN\x1b[0m   \x1b[38;5;100mNNP\x1b[0m   \x1b[38;5;100mNounType=prop|N\x1b[0m   \x1b[38;5;196mGPE   \x1b[0m\n\x1b[38;5;2m╚════>\x1b[0m   \x1b[38;5;2mpunct   \x1b[0m   9       .         .         \x1b[38;5;100mPUNCT\x1b[0m   \x1b[38;5;100m.  \x1b[0m   \x1b[38;5;100mPunctType=peri \x1b[0m   \x1b[38;5;196m      \x1b[0m\n\n\n\x1b[38;5;2mtree\x1b[0m   \x1b[38;5;2mdep  \x1b[0m   index   text    lemma   \x1b[38;5;100mpos  \x1b[0m   \x1b[38;5;100mtag\x1b[0m   \x1b[38;5;100mmorph          \x1b[0m   \x1b[38;5;196ment\x1b[0m\n\x1b[38;5;2m----\x1b[0m   \x1b[38;5;2m-----\x1b[0m   -----   -----   -----   \x1b[38;5;100m-----\x1b[0m   \x1b[38;5;100m---\x1b[0m   \x1b[38;5;100m---------------\x1b[0m   \x1b[38;5;196m---\x1b[0m\n\x1b[38;5;2m  ╔>\x1b[0m   \x1b[38;5;2mnsubj\x1b[0m   10      She     she     \x1b[38;5;100mPRON \x1b[0m   \x1b[38;5;100mPRP\x1b[0m   \x1b[38;5;100mCase=Nom|Gender\x1b[0m   \x1b[38;5;196m   \x1b[0m\n\x1b[38;5;2m  ╠═\x1b[0m   \x1b[38;5;2mROOT \x1b[0m   11      loved   love    \x1b[38;5;100mVERB \x1b[0m   \x1b[38;5;100mVBD\x1b[0m   \x1b[38;5;100mTense=Past|Verb\x1b[0m   \x1b[38;5;196m   \x1b[0m\n\x1b[38;5;2m  ╠>\x1b[0m   \x1b[38;5;2mdobj \x1b[0m   12      it      it      \x1b[38;5;100mPRON \x1b[0m   \x1b[38;5;100mPRP\x1b[0m   \x1b[38;5;100mCase=Acc|Gender\x1b[0m   \x1b[38;5;196m   \x1b[0m\n\x1b[38;5;2m  ╚>\x1b[0m   \x1b[38;5;2mpunct\x1b[0m   13      .       .       \x1b[38;5;100mPUNCT\x1b[0m   \x1b[38;5;100m.  \x1b[0m   \x1b[38;5;100mPunctType=peri \x1b[0m   \x1b[38;5;196m   \x1b[0m\n\n"
        if SUPPORTS_ANSI
        else "\n  tree   dep        index   text      lemma     pos     tag   morph             ent   \n------   --------   -----   -------   -------   -----   ---   ---------------   ------\n  ╔>╔═   poss       0       Sarah     sarah     PROPN   NNP   NounType=prop|N   PERSON\n  ║ ╚>   case       1       's        's        PART    POS   Poss=yes                \n╔>╚═══   nsubj      2       sister    sister    NOUN    NN    Number=sing             \n╠═════   ROOT       3       flew      fly       VERB    VBD   Tense=past|Verb         \n╠>╔═══   prep       4       to        to        ADP     IN                            \n║ ║ ╔>   compound   5       Silicon   silicon   PROPN   NNP   NounType=prop|N   GPE   \n║ ╚>╚═   pobj       6       Valley    valley    PROPN   NNP   NounType=prop|N   GPE   \n╠══>╔═   prep       7       via       via       ADP     IN                            \n║   ╚>   pobj       8       London    london    PROPN   NNP   NounType=prop|N   GPE   \n╚════>   punct      9       .         .         PUNCT   .     PunctType=peri          \n\n\ntree   dep     index   text    lemma   pos     tag   morph             ent\n----   -----   -----   -----   -----   -----   ---   ---------------   ---\n  ╔>   nsubj   10      She     she     PRON    PRP   Case=Nom|Gender      \n  ╠═   ROOT    11      loved   love    VERB    VBD   Tense=Past|Verb      \n  ╠>   dobj    12      it      it      PRON    PRP   Case=Acc|Gender      \n  ╚>   punct   13      .       .       PUNCT   .     PunctType=peri       \n\n"
    )
    assert render_table(fully_featured_doc_two_sentences, formats, spacing=3) == target
    assert (
        render_table(
            fully_featured_doc_two_sentences, formats, spacing=3, start_i=3, length=300
        )
        == target
    )
    assert (
        render_table(
            fully_featured_doc_two_sentences, formats, spacing=3, start_i=3, length=9
        )
        == target
    )


def test_viz_rich_render_table_start(
    fully_featured_doc_two_sentences,
):
    formats = [
        AttributeFormat("tree_left", name="tree", aligns="r", fg_color=2),
        AttributeFormat("dep_", name="dep", fg_color=2),
        AttributeFormat("i", name="index", aligns="r"),
        AttributeFormat("text", name="text"),
        AttributeFormat("lemma_", name="lemma"),
        AttributeFormat("pos_", name="pos", fg_color=100),
        AttributeFormat("tag_", name="tag", fg_color=100),
        AttributeFormat("morph", name="morph", fg_color=100, max_width=15),
        AttributeFormat(
            "ent_type_",
            name="ent",
            fg_color=196,
            value_dep_fg_colors={"PERSON": 50},
            value_dep_bg_colors={"PERSON": 12},
        ),
    ]
    print(
        render_table(fully_featured_doc_two_sentences, formats, spacing=3, start_i=11)
    )
    print(
        repr(
            render_table(
                fully_featured_doc_two_sentences, formats, spacing=3, start_i=11
            )
        )
    )
    target = (
        "\n\x1b[38;5;2mtree\x1b[0m   \x1b[38;5;2mdep  \x1b[0m   index   text    lemma   \x1b[38;5;100mpos  \x1b[0m   \x1b[38;5;100mtag\x1b[0m   \x1b[38;5;100mmorph          \x1b[0m   \x1b[38;5;196ment\x1b[0m\n\x1b[38;5;2m----\x1b[0m   \x1b[38;5;2m-----\x1b[0m   -----   -----   -----   \x1b[38;5;100m-----\x1b[0m   \x1b[38;5;100m---\x1b[0m   \x1b[38;5;100m---------------\x1b[0m   \x1b[38;5;196m---\x1b[0m\n\x1b[38;5;2m  ╔>\x1b[0m   \x1b[38;5;2mnsubj\x1b[0m   10      She     she     \x1b[38;5;100mPRON \x1b[0m   \x1b[38;5;100mPRP\x1b[0m   \x1b[38;5;100mCase=Nom|Gender\x1b[0m   \x1b[38;5;196m   \x1b[0m\n\x1b[38;5;2m  ╠═\x1b[0m   \x1b[38;5;2mROOT \x1b[0m   11      loved   love    \x1b[38;5;100mVERB \x1b[0m   \x1b[38;5;100mVBD\x1b[0m   \x1b[38;5;100mTense=Past|Verb\x1b[0m   \x1b[38;5;196m   \x1b[0m\n\x1b[38;5;2m  ╠>\x1b[0m   \x1b[38;5;2mdobj \x1b[0m   12      it      it      \x1b[38;5;100mPRON \x1b[0m   \x1b[38;5;100mPRP\x1b[0m   \x1b[38;5;100mCase=Acc|Gender\x1b[0m   \x1b[38;5;196m   \x1b[0m\n\x1b[38;5;2m  ╚>\x1b[0m   \x1b[38;5;2mpunct\x1b[0m   13      .       .       \x1b[38;5;100mPUNCT\x1b[0m   \x1b[38;5;100m.  \x1b[0m   \x1b[38;5;100mPunctType=peri \x1b[0m   \x1b[38;5;196m   \x1b[0m\n\n"
        if SUPPORTS_ANSI
        else "\ntree   dep     index   text    lemma   pos     tag   morph             ent\n----   -----   -----   -----   -----   -----   ---   ---------------   ---\n  ╔>   nsubj   10      She     she     PRON    PRP   Case=Nom|Gender      \n  ╠═   ROOT    11      loved   love    VERB    VBD   Tense=Past|Verb      \n  ╠>   dobj    12      it      it      PRON    PRP   Case=Acc|Gender      \n  ╚>   punct   13      .       .       PUNCT   .     PunctType=peri       \n\n"
    )
    assert (
        render_table(fully_featured_doc_two_sentences, formats, spacing=3, start_i=11)
        == target
    )
    assert (
        render_table(
            fully_featured_doc_two_sentences,
            formats,
            spacing=3,
            start_i=11,
            search_attr_name="pos",
            search_attr_value="VERB",
        )
        == target
    )
    assert (
        render_table(
            fully_featured_doc_two_sentences,
            formats,
            spacing=3,
            start_i=2,
            search_attr_name="lemma",
            search_attr_value="love",
        )
        == target
    )
    assert (
        render_table(
            fully_featured_doc_two_sentences,
            formats,
            spacing=3,
            search_attr_name="lemma",
            search_attr_value="love",
        )
        == target
    )
    assert (
        render_table(
            fully_featured_doc_two_sentences,
            formats,
            spacing=3,
            start_i=2,
            length=3,
            search_attr_name="lemma",
            search_attr_value="love",
        )
        == target
    )
    assert (
        render_table(
            fully_featured_doc_two_sentences,
            formats,
            spacing=3,
            search_attr_name="lemma_",
            search_attr_value="love",
        )
        == target
    )
    assert (
        render_table(
            fully_featured_doc_two_sentences,
            formats,
            spacing=3,
            search_attr_name="lemma",
            search_attr_value="lovef",
        )
        == ""
    )
    assert (
        render_table(
            fully_featured_doc_two_sentences,
            formats,
            spacing=3,
            search_attr_name="lemma_",
            search_attr_value="lovef",
        )
        == ""
    )
    assert (
        render_table(
            fully_featured_doc_two_sentences,
            formats,
            spacing=3,
            search_attr_name="lemmaa",
            search_attr_value="love",
        )
        == ""
    )
    assert (
        render_table(
            fully_featured_doc_two_sentences,
            formats,
            spacing=3,
            start_i=50,
            search_attr_name="lemma",
            search_attr_value="love",
        )
        == ""
    )


def test_viz_rich_render_table_end(
    fully_featured_doc_two_sentences,
):
    formats = [
        AttributeFormat("tree_left", name="tree", aligns="r", fg_color=2),
        AttributeFormat("dep_", name="dep", fg_color=2),
        AttributeFormat("i", name="index", aligns="r"),
        AttributeFormat("text", name="text"),
        AttributeFormat("lemma_", name="lemma"),
        AttributeFormat("pos_", name="pos", fg_color=100),
        AttributeFormat("tag_", name="tag", fg_color=100),
        AttributeFormat("morph", name="morph", fg_color=100, max_width=15),
        AttributeFormat(
            "ent_type_",
            name="ent",
            fg_color=196,
            value_dep_fg_colors={"PERSON": 50},
            value_dep_bg_colors={"PERSON": 12},
        ),
    ]
    target = (
        "\n\x1b[38;5;2m  tree\x1b[0m   \x1b[38;5;2mdep     \x1b[0m   index   text      lemma     \x1b[38;5;100mpos  \x1b[0m   \x1b[38;5;100mtag\x1b[0m   \x1b[38;5;100mmorph          \x1b[0m   \x1b[38;5;196ment   \x1b[0m\n\x1b[38;5;2m------\x1b[0m   \x1b[38;5;2m--------\x1b[0m   -----   -------   -------   \x1b[38;5;100m-----\x1b[0m   \x1b[38;5;100m---\x1b[0m   \x1b[38;5;100m---------------\x1b[0m   \x1b[38;5;196m------\x1b[0m\n\x1b[38;5;2m  ╔>╔═\x1b[0m   \x1b[38;5;2mposs    \x1b[0m   0       Sarah     sarah     \x1b[38;5;100mPROPN\x1b[0m   \x1b[38;5;100mNNP\x1b[0m   \x1b[38;5;100mNounType=prop|N\x1b[0m   \x1b[38;5;196m\x1b[38;5;50;48;5;12mPERSON\x1b[0m\x1b[0m\n\x1b[38;5;2m  ║ ╚>\x1b[0m   \x1b[38;5;2mcase    \x1b[0m   1       's        's        \x1b[38;5;100mPART \x1b[0m   \x1b[38;5;100mPOS\x1b[0m   \x1b[38;5;100mPoss=yes       \x1b[0m   \x1b[38;5;196m      \x1b[0m\n\x1b[38;5;2m╔>╚═══\x1b[0m   \x1b[38;5;2mnsubj   \x1b[0m   2       sister    sister    \x1b[38;5;100mNOUN \x1b[0m   \x1b[38;5;100mNN \x1b[0m   \x1b[38;5;100mNumber=sing    \x1b[0m   \x1b[38;5;196m      \x1b[0m\n\x1b[38;5;2m╠═════\x1b[0m   \x1b[38;5;2mROOT    \x1b[0m   3       flew      fly       \x1b[38;5;100mVERB \x1b[0m   \x1b[38;5;100mVBD\x1b[0m   \x1b[38;5;100mTense=past|Verb\x1b[0m   \x1b[38;5;196m      \x1b[0m\n\x1b[38;5;2m╠>╔═══\x1b[0m   \x1b[38;5;2mprep    \x1b[0m   4       to        to        \x1b[38;5;100mADP  \x1b[0m   \x1b[38;5;100mIN \x1b[0m   \x1b[38;5;100m               \x1b[0m   \x1b[38;5;196m      \x1b[0m\n\x1b[38;5;2m║ ║ ╔>\x1b[0m   \x1b[38;5;2mcompound\x1b[0m   5       Silicon   silicon   \x1b[38;5;100mPROPN\x1b[0m   \x1b[38;5;100mNNP\x1b[0m   \x1b[38;5;100mNounType=prop|N\x1b[0m   \x1b[38;5;196mGPE   \x1b[0m\n\x1b[38;5;2m║ ╚>╚═\x1b[0m   \x1b[38;5;2mpobj    \x1b[0m   6       Valley    valley    \x1b[38;5;100mPROPN\x1b[0m   \x1b[38;5;100mNNP\x1b[0m   \x1b[38;5;100mNounType=prop|N\x1b[0m   \x1b[38;5;196mGPE   \x1b[0m\n\x1b[38;5;2m╠══>╔═\x1b[0m   \x1b[38;5;2mprep    \x1b[0m   7       via       via       \x1b[38;5;100mADP  \x1b[0m   \x1b[38;5;100mIN \x1b[0m   \x1b[38;5;100m               \x1b[0m   \x1b[38;5;196m      \x1b[0m\n\x1b[38;5;2m║   ╚>\x1b[0m   \x1b[38;5;2mpobj    \x1b[0m   8       London    london    \x1b[38;5;100mPROPN\x1b[0m   \x1b[38;5;100mNNP\x1b[0m   \x1b[38;5;100mNounType=prop|N\x1b[0m   \x1b[38;5;196mGPE   \x1b[0m\n\x1b[38;5;2m╚════>\x1b[0m   \x1b[38;5;2mpunct   \x1b[0m   9       .         .         \x1b[38;5;100mPUNCT\x1b[0m   \x1b[38;5;100m.  \x1b[0m   \x1b[38;5;100mPunctType=peri \x1b[0m   \x1b[38;5;196m      \x1b[0m\n\n"
        if SUPPORTS_ANSI
        else "\n  tree   dep        index   text      lemma     pos     tag   morph             ent   \n------   --------   -----   -------   -------   -----   ---   ---------------   ------\n  ╔>╔═   poss       0       Sarah     sarah     PROPN   NNP   NounType=prop|N   PERSON\n  ║ ╚>   case       1       's        's        PART    POS   Poss=yes                \n╔>╚═══   nsubj      2       sister    sister    NOUN    NN    Number=sing             \n╠═════   ROOT       3       flew      fly       VERB    VBD   Tense=past|Verb         \n╠>╔═══   prep       4       to        to        ADP     IN                            \n║ ║ ╔>   compound   5       Silicon   silicon   PROPN   NNP   NounType=prop|N   GPE   \n║ ╚>╚═   pobj       6       Valley    valley    PROPN   NNP   NounType=prop|N   GPE   \n╠══>╔═   prep       7       via       via       ADP     IN                            \n║   ╚>   pobj       8       London    london    PROPN   NNP   NounType=prop|N   GPE   \n╚════>   punct      9       .         .         PUNCT   .     PunctType=peri          \n\n"
    )

    assert (
        render_table(fully_featured_doc_two_sentences, formats, spacing=3, start_i=2)
        == target
    )
    assert (
        render_table(
            fully_featured_doc_two_sentences, formats, spacing=3, start_i=2, length=3
        )
        == target
    )
    assert (
        render_table(fully_featured_doc_two_sentences, formats, spacing=3, length=3)
        == target
    )
    assert (
        render_table(
            fully_featured_doc_two_sentences,
            formats,
            spacing=3,
            search_attr_name="pos",
            search_attr_value="VERB",
        )
        == target
    )
