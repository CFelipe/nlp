# 96 quite bitter beings

import pickle
from grammar import dd, Node, Rule, Grammar, PICKLE_FILE

def cky_parse(grammar: Grammar, sentence: list) -> list:
    table = []
    for i in range(len(sentence.split())):
        table.append([[] for _ in range(i + 1)])
    print(table)

    words = sentence.split()
    for j, word in enumerate(words):
        print(word)
        for rule in grammar.words_pos[word]:
            print(rule)
        print("---")
            # table[j - 1][j].append(rule)

    # for i in reversed(range(j - 2)):
    #     for k in range(i + 1, j -1):
    #         for rules -> BC and B in table[i, k] and C in table[k, j]:
    #             table[i, j].append(rule)

if __name__ == "__main__":
    with open(PICKLE_FILE, 'rb') as grammar_file:
        grammar = pickle.load(grammar_file)
        sentence = "Book me the flight to Houston"

        cky_parse(grammar, sentence)
