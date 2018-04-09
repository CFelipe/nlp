import common
import pickle
import copy
from pathlib import Path

class ViterbiTagger(common.Tagger):
    PICKLE_FILE = "models/viterbi-model.pkl"

    START_STR = "START"
    END_STR = "END"
    UNKNOWN_STR = "-UNKNOWN_WORD-"
    UNKNOWN_TRESHOLD = 1

    def train(self, corpus_filename: str):
        """Calculates emission and transition model.

        t means tag, w means word.


        Emission:   P(w[i] | t[i]) =   C(t[i], w[i]) / C(t[i])
        Transition: P(t[i] | t[i-1]) = C(t[i-1], t[i]) / C(t[i-1])

        Where C(t) counts the occurrences of t
        """

        model = {}
        pos_words = {}

        p = Path(corpus_filename)
        with open(corpus_filename) as f:
            parenstack = [];
            bigrams = {}
            bigrams[self.END_STR] = {}
            word_counts = {}

            for line in f:
                tokens = common.tokenize(line)
                tokens_in_node = []
                for token in tokens:
                    if token == '(':
                        parenstack.append('(')
                        tokens_in_node = []
                    elif token == 'S':
                        prev = self.START_STR
                    elif token == ')':
                        parenstack.pop()
                        if not parenstack:
                            if not prev in bigrams[self.END_STR]:
                                bigrams[self.END_STR][prev] = 1
                            else:
                                bigrams[self.END_STR][prev] += 1

                        elif len(tokens_in_node) == 2:
                            pos, word = tokens_in_node

                            if pos != "-NONE-":
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

                                if not word in word_counts:
                                    word_counts[word] = 1
                                else:
                                    word_counts[word] += 1
                    else:
                        tokens_in_node.append(token)

            # normalize transition model
            for pos, d in bigrams.items():
                total = sum(d.values())
                for prev, count in d.items():
                    bigrams[pos][prev] = count / total

            # rare words are counted as a single word
            pos_words2 = copy.deepcopy(pos_words)

            for pos, d in pos_words.items():
                for word, count in d.items():
                    if count <= self.UNKNOWN_TRESHOLD:
                        pos_words2[pos].pop(word)
                        if not self.UNKNOWN_STR in pos_words2[pos]:
                            pos_words2[pos][self.UNKNOWN_STR] = 1
                        else:
                            pos_words2[pos][self.UNKNOWN_STR] += 1

            pos_words = pos_words2

            # normalize emission model
            for pos, d in pos_words.items():
                total = sum(d.values())
                for word, count in d.items():
                    pos_words[pos][word] = count / total

            model["bigrams"] = bigrams
            model["pos_words"] = pos_words

            p = Path(self.PICKLE_FILE)
            with p.open('wb') as output_file:
                pickle.dump(model, output_file, pickle.HIGHEST_PROTOCOL)

    def get_bigram(self, tag: str, prev: str):
        if prev in self.model["bigrams"][tag].keys():
            return self.model["bigrams"][tag][prev]
        else:
            return 0

    def get_pos_words(self, tag: str, word: str):
        if word in self.model["pos_words"][tag].keys():
            return self.model["pos_words"][tag][word]
        else:
            return 0

    def unknown_word(self, word: str) -> bool:
        for tag in self.model["pos_words"].keys():
            if self.get_pos_words(tag, word) > 0:
                return False

        return True

    def info_word(self, word: str, model: dict):
        for tag in model["pos_words"].keys():
            if get_pos_words(model["pos_words"], tag, word) > 0:
                print(tag, self.get_pos_words(tag, word))

    def tag_sentence(self, sentence: str) -> str:
        """Tags sentence using the Viterbi algorithm"""

        self.load_model()

        words = sentence.split()

        p = self.model
        bigrams = p["bigrams"]
        pos_words = p["pos_words"]
        tags = p["pos_words"].keys()

        # initialization step
        first_word = words[0] if not self.unknown_word(words[0]) else self.UNKNOWN_STR

        viterbi = {}
        backpointer = {}
        for tag in tags:
            viterbi[tag] = [[] for _ in range(len(words))]
            backpointer[tag] = [[] for _ in range(len(words))]

            viterbi[tag][0] = self.get_bigram(tag, self.START_STR) * \
                              self.get_pos_words(tag, first_word)
            backpointer[tag][0] = 0

        # recursion step
        for idx_word, word in enumerate(words[1:], 1):
            if self.unknown_word(word):
                word = self.UNKNOWN_STR

            max_p_word = 0

            for tag in tags:
                max_p = 0.0
                max_tag = 0

                max_bp = 0.0 # backpointer doesn't care about the emission
                argmax_bp = 0

                for prev_tag in tags:
                    p_tag = viterbi[prev_tag][idx_word - 1] * \
                            self.get_bigram(tag, prev_tag) * \
                            self.get_pos_words(tag, word)

                    if p_tag > max_p:
                        max_p = p_tag

                    bp_tag = viterbi[prev_tag][idx_word - 1] * \
                             self.get_bigram(tag, prev_tag)

                    if bp_tag > max_bp:
                        max_bp = bp_tag
                        argmax_bp = prev_tag

                viterbi[tag][idx_word] = max_p
                backpointer[tag][idx_word] = argmax_bp

                if max_p > max_p_word:
                    max_p_word = max_p

            if max_p_word == 0: # all failed
                # backpointer is argmax viterbi

                for tag in tags:
                    max_bigram_p = 0
                    argmax_bigram_p = 0

                    max_viterbi_p = 0
                    argmax_viterbi_p = 0

                    for prev_tag in tags:
                        bigram_p = self.get_bigram(tag, prev_tag)
                        viterbi_p = viterbi[prev_tag][idx_word - 1]

                        if bigram_p > max_bigram_p:
                            max_bigram_p = bigram_p
                            argmax_bigram_p = prev_tag

                        if viterbi_p > max_viterbi_p:
                            max_viterbi_p = viterbi_p
                            argmax_viterbi_p = prev_tag

                    viterbi[tag][idx_word] = max_viterbi_p
                    backpointer[tag][idx_word] = argmax_viterbi_p

        # termination step
        max_p = 0
        argmax_bp = 0

        for tag in tags:
            p_tag = viterbi[tag][len(words) - 1] * \
                    self.get_bigram(self.END_STR, tag)

            if p_tag > max_p:
                max_p = p_tag
                argmax_bp = tag

        viterbi[self.END_STR] = max_p
        backpointer[self.END_STR] = argmax_bp

        # print(viterbi)
        # print(backpointer)
        # print(sentence)

        # backtrace
        last_tag = backpointer[self.END_STR]
        pos_tags = [last_tag]

        try:
            for idx in range(len(words) - 1):
                pos_tags.append(backpointer[last_tag][len(words) - 1 - idx])
                last_tag = pos_tags[-1]
        except KeyError as e:
            print("Key error in sentence: ", sentence)

        pos_tags.reverse()
        words_tags = ["({} {})".format(pos_tag, word) for pos_tag, word in zip(pos_tags, words)]
        return "(S {})".format(" ".join(words_tags))
