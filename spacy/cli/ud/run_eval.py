import os
import spacy
import time
import re

from spacy.cli.ud import conll17_ud_eval
from spacy.cli.ud.ud_train import write_conllu

# TODO: remove hardcoded path
ud_location = os.path.join('C:', os.sep, 'Users', 'Sofie', 'Documents', 'data', 'UD_2_3', 'ud-treebanks-v2.3')
ud_version = '2.3'
ud_folder = 'UD_English-'
ud_lang = 'en_'

space_re = re.compile("\s+")


def get_training_path(treebank, conllu=False):
    ud_path = os.path.join(ud_location, ud_folder + treebank)
    train_file = os.path.join(ud_path, ud_lang + treebank.lower() + '-ud-train.txt')
    if conllu:
        train_file = train_file.replace('.txt', '.conllu')
    return train_file


def load_model(modelname):
    """ Load a specific model """
    return spacy.load(modelname)


def load_english_model():
    """ Load a generic English model """
    from spacy.lang.en import English
    nlp = English()
    nlp.add_pipe(nlp.create_pipe('sentencizer'))
    return nlp


def split_text(text):
    return [space_re.sub(" ", par.strip()) for par in text.split("\n\n")]


if __name__ == "__main__":
    # RUN PARAMETERS
    run_eval = True
    my_model = 'en_core_web_sm'

    # STEP 0 : loading raw text
    # English treebanks: ESL, EWT, GUM, LinES, ParTUT, PUD
    # ESL does not contain the actual texts, PUD does not contain a train/dev portion
    # EWT is the biggest one, ParTUT is the only one with fusion tokens
    my_treebank = "EWT"
    train_path = get_training_path(my_treebank, conllu=False)
    with open(train_path, 'r', encoding='utf-8') as fin:
        flat_text = fin.read()

    # STEP 1: load model
    start = time.time()
    nlp = load_model(modelname=my_model)
    # nlp = load_english_model()
    end_loading = time.time()
    loading_time = end_loading - start

    # STEP 2: tokenize text
    texts = split_text(flat_text)
    docs = list(nlp.pipe(texts))
    end_tokenization = time.time()
    tokenization_time = end_tokenization - end_loading

    # STEP 3: record stats and timings
    gold_file = open(get_training_path(my_treebank, conllu=True), 'r', encoding='utf-8')
    gold_ud = conll17_ud_eval.load_conllu(gold_file)
    tokens_per_s = int(len(gold_ud.tokens) / tokenization_time)

    print_header = ['train_path', 'gold_tokens', 'model', 'loading_time', 'tokenization_time', 'tokens_per_s']
    print_string = [os.path.basename(train_path), len(gold_ud.tokens), my_model,
                    "%.2f" % loading_time, "%.2f" % tokenization_time, tokens_per_s]

    # STEP 4: evaluate predicted tokens and features
    if run_eval:
        output_path = os.path.join(os.path.dirname(__file__), 'nlp_output_english.conllu')
        with open(output_path, "w", encoding="utf8") as out_file:
            write_conllu(docs, out_file)
        with open(output_path, "r", encoding="utf8") as sys_file:
            sys_ud = conll17_ud_eval.load_conllu(sys_file)
        scores = conll17_ud_eval.evaluate(gold_ud, sys_ud)

        # fixed order for normalized printing
        for score_name in ['Tokens', 'Words', 'Lemmas', 'Sentences', 'UPOS', 'XPOS', 'Feats', 'AllTags', 'UAS', 'LAS']:
            score = scores[score_name]
            print_string.extend(["%.2f" % score.precision,
                                 "%.2f" % score.recall,
                                 "%.2f" % score.f1])
            print_string.append("-" if score.aligned_accuracy is None else "%.2f" % score.aligned_accuracy)
            print_header.extend([score_name + '_p', score_name + '_r', score_name + '_F', score_name + '_acc'])

    # STEP 5: print the results
    print(" Loading model took {} seconds: {}".format(loading_time, nlp))
    print(" Tokenizing text took {} seconds".format(tokenization_time))
    print(" Tokens per second: {}".format(tokens_per_s))
    print()

    print(';'.join(map(str, print_header)))
    print(';'.join(map(str, print_string)))

