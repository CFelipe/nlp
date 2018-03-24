import common
import pickle
from pathlib import Path

class NaiveTagger(common.Tagger):
    PICKLE_FILE = "models/naive-model.pkl"

    def train(self, corpus_filename: str):
        word_freq = {}

        p = Path(corpus_filename)
        with open(corpus_filename) as f:
            parenstack = [];
            words_pos = []
            line_number = 1

            for line in f:
                line_number += 1
                tokens = common.tokenize(line)
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

            p = Path(self.PICKLE_FILE)
            with p.open('wb') as output_file:
                pickle.dump(word_freq, output_file, pickle.HIGHEST_PROTOCOL)

    def tag_sentence(self, sentence: str) -> str:
        """Tags sentence using the most frequent POS for each word"""

        self.load_model()

        tags = []

        for word in sentence.split():
            if word in self.model:
                pos = max(self.model[word], key=self.model[word].get)
            else:
                pos = "NN"
            tags.append(("({} {})".format(pos, word)))
        return "(S {})".format(" ".join(tags))
