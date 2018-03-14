import json
import pickle
import argparse

def tokenize(chars: str) -> list:
    "Convert a string of characters into a list of tokens."
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()

def frequencies_from_file(filename: str):
    word_freq = {}
    with open(filename) as f:
        parenstack = [];
        words_pos = []
        line_number = 1

        for line in f:
            line_number += 1
            tokens = tokenize(line)
            tokens_in_node = []
            for token in tokens:
                if token == '(':
                    parenstack.append('(')
                    tokens_in_node = []
                elif token == ')':
                    parenstack.pop()
                    if len(tokens_in_node) == 2:
                        words_pos.append(tuple(tokens_in_node))
                        pos, word = tokens_in_node
                        if not word in word_freq:
                            word_freq[word] = {}
                            word_freq[word][pos] = 1
                        else:
                            if not pos in word_freq[word]:
                                word_freq[word][pos] = 1
                            else:
                                word_freq[word][pos] += 1
                            tokens_in_node = []
                else:
                    tokens_in_node.append(token)

        #print(words_pos)
        with open('frequencies.pkl', 'wb') as output_file:
            pickle.dump(word_freq, output_file, pickle.HIGHEST_PROTOCOL)

def read_frequencies() -> dict:
    with open('frequencies.pkl', 'rb') as input_file:
        word_freq = pickle.load(input_file)
        #print(json.dumps(word_freq, indent=1))
        return word_freq

# the tree-to-sentence program takes care of that, but it's nice to have anyways
def treat_punctuation(sentence: str) -> str:
    for punctuation in ".,;:$%":
        sentence = sentence.replace(punctuation, " {} ".format(punctuation))
    return sentence

def tag_sentence(sentence: str, sep: str=" ") -> str:
    tags = []

    for word in sentence.split():
        if word in pos_frequencies:
            pos = max(pos_frequencies[word], key=pos_frequencies[word].get)
        else:
            pos = "NN"
        tags.append(("({} {})".format(pos, word)))
    return "(S {})".format(sep.join(tags))

def tag_file(input_filename: str):
    with open(input_filename,          'r') as sentences_file, \
         open(input_filename + ".tst", 'w') as output_file:
        for sentence in sentences_file:
            output_file.write(tag_sentence(sentence) + "\n")

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description='Parts-of-speech tagger')
    argparser.add_argument("input_file", help="File with sentences separated by newlines")
    args = argparser.parse_args()

    pos_frequencies = read_frequencies()

    tag_file(args.input_file)
    #frequencies_from_file("penn/traindata")

# test with `evalb -p collins.prm gold.gld test.tst`
# test with `evalb -p collins.prm sentences23.gold sentences23.tst`
