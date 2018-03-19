import json
import pickle
import argparse
import time

START_STR = "START"
END_STR = "END"

def tokenize(chars: str) -> list:
    "Convert a string of characters into a list of tokens."
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()

def frequencies_from_file(filename: str):
    """Calculates emission and transition probabilities.

    t means tag, w means word.

    Emission:   P(w[i] | t[i]) =   C(t[i], w[i]) / C(t[i])
    Transition: P(t[i] | t[i-1]) = C(t[i-1], t[i]) / C(t[i-1])

    Where C(t) counts the occurrences of t
    """

    probabilities = {}
    pos_words = {}
    with open(filename) as f:
        parenstack = [];
        bigrams = {}
        bigrams[END_STR] = {}

        for line in f:
            tokens = tokenize(line)
            tokens_in_node = []
            for token in tokens:
                if token == '(':
                    parenstack.append('(')
                    tokens_in_node = []
                elif token == 'S':
                    prev = START_STR
                elif token == ')':
                    parenstack.pop()
                    if not parenstack:
                        if not prev in bigrams[END_STR]:
                            bigrams[END_STR][prev] = 1
                        else:
                            bigrams[END_STR][prev] += 1

                    elif len(tokens_in_node) == 2:
                        pos, word = tokens_in_node

                        if not pos in bigrams:
                            bigrams[pos] = {}

                        if not prev in bigrams[pos]:
                            bigrams[pos][prev] = 1
                        else:
                            bigrams[pos][prev] += 1

                        prev = pos

                        if not pos in pos_words:
                            pos_words[pos] = {}
                            pos_words[pos][word] = 1
                        else:
                            if not word in pos_words[pos]:
                                pos_words[pos][word] = 1
                            else:
                                pos_words[pos][word] += 1
                            tokens_in_node = []
                else:
                    tokens_in_node.append(token)

        # normalize transition probabilities
        for pos, d in bigrams.items():
            total = sum(d.values())
            for prev, count in d.items():
                bigrams[pos][prev] = count / total

        # normalize emission probabilities
        for pos, d in pos_words.items():
            total = sum(d.values())
            for word, count in d.items():
                pos_words[pos][word] = count / total

        probabilities["bigrams"] = bigrams
        probabilities["pos_words"] = pos_words

        print(json.dumps(bigrams, indent=1))

        with open('probabilities-viterbi.pkl', 'wb') as output_file:
            pickle.dump(probabilities, output_file, pickle.HIGHEST_PROTOCOL)

def read_frequencies() -> dict:
    with open('probabilities-viterbi.pkl', 'rb') as input_file:
        probabilities = pickle.load(input_file)
        return probabilities

def get_bigram(d: dict, tag: str, prev: str):
    if prev in d[tag].keys():
        return d[tag][prev]
    else:
        return 0

def get_pos_words(d: dict, tag: str, word: str):
    if word in d[tag].keys():
        return d[tag][word]
    else:
        return 0

def unknown_word(word: str, probabilities: dict) -> bool:
    for tag in probabilities["pos_words"].keys():
        if get_pos_words(probabilities["pos_words"], tag, word) > 0:
            return False

    return True

def tag_sentence(sentence: str, probabilities: dict, sep: str=" ",) -> str:
    """Tags sentence using the Viterbi algorithm"""

    #print(sentence)
    words = sentence.split()

    p = probabilities
    bigrams = p["bigrams"]
    pos_words = p["pos_words"]
    tags = p["pos_words"].keys()

    # initialization step
    first_word = words[0] if not unknown_word(words[0], p) else "man"

    viterbi = {}
    backpointer = {}
    for tag in tags:
        viterbi[tag] = [[] for _ in range(len(words))]
        backpointer[tag] = [[] for _ in range(len(words))]

        viterbi[tag][0] = get_bigram(bigrams, tag, START_STR) * \
                          get_pos_words(pos_words, tag, first_word)
        backpointer[tag][0] = 0

    # recursion step
    for idx_word, word in enumerate(words[1:], 1):
        if unknown_word(word, p):
            word = "man"

        for tag in tags:
            max_p = 0.0
            max_tag = 0

            max_bp = 0.0 # backpointer doesn't care about the emission
            argmax_bp = 0

            for prev_tag in tags:
                p_tag = viterbi[prev_tag][idx_word - 1] * \
                        get_bigram(bigrams, tag, prev_tag) * \
                        get_pos_words(pos_words, tag, word)

                if p_tag > max_p:
                    max_p = p_tag

                bp_tag = viterbi[prev_tag][idx_word - 1] * \
                         get_bigram(bigrams, tag, prev_tag)

                if bp_tag > max_bp:
                    max_bp = bp_tag
                    argmax_bp = prev_tag

            viterbi[tag][idx_word] = max_p
            backpointer[tag][idx_word] = argmax_bp

    # termination step
    max_p = 0
    argmax_bp = 0

    for tag in tags:
        p_tag = viterbi[tag][len(words) - 1] * \
                get_bigram(bigrams, END_STR, tag)

        if p_tag > max_p:
            max_p = p_tag
            argmax_bp = tag

    viterbi[END_STR] = max_p
    backpointer[END_STR] = argmax_bp

    # print(json.dumps(viterbi, indent=1))
    # print(json.dumps(backpointer, indent=1))
    # print(viterbi)
    # print(backpointer)
    # print(sentence)

    # backtrace
    last_tag = backpointer[END_STR]
    pos_tags = [last_tag]

    try:
        for idx in range(len(words) - 1):
            pos_tags.append(backpointer[last_tag][len(words) - 1 - idx])
            last_tag = pos_tags[-1]
    except KeyError as e:
        print(e)
        print(idx)
        print(backpointer)
        print("Key error in sentence: ", sentence)

    pos_tags.reverse()
    words_tags = ["({} {})".format(pos_tag, word) for pos_tag, word in zip(pos_tags, words)]
    return "(S {})".format(sep.join(words_tags))

def tag_file(input_filename: str, probabilities):
    with open(input_filename,          'r') as sentences_file, \
         open(input_filename + ".tst", 'w') as output_file:
        for sentence in sentences_file:
            output_file.write(tag_sentence(sentence, probabilities) + "\n")

if __name__ == "__main__":
    probabilities = read_frequencies()

    argparser = argparse.ArgumentParser(description='Parts-of-speech tagger')
    argparser.add_argument("-s", "--sentence",   help="Tag a sentence")
    argparser.add_argument("-i", "--input_file", help="Input file")
    argparser.add_argument("-t", "--train_file", help="Training file")
    args = argparser.parse_args()

    if args.input_file:
        print("input file")
        tag_file(args.input_file, probabilities)
    elif args.sentence:
        print(tag_sentence(args.sentence, probabilities))
    elif args.train_file:
        # frequencies_from_file("penn/traindata")
        print("train file")


