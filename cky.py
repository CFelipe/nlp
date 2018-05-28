# 96 quite bitter beings

import pickle
from grammar import Node, Rule, Grammar, PICKLE_FILE

table = []
words = "Book the flight to Houston"
for i in range(len(words.split())):
    table.append([[] for _ in range(i + 1)])
print(table)

def cky_parse(grammar: Grammar, words: list) -> list:
    pass

# for j in len(words):
#     for all rules that make this word:
#         table[j - 1][j].append(rule)

    # for i in reversed(range(j - 2)):
    #     for k in range(i + 1, j -1):
    #         for rules -> BC and B in table[i, k] and C in table[k, j]:
    #             table[i, j].append(rule)


if __name__ == "__main__":
    print(PICKLE_FILE)
    with open(PICKLE_FILE, 'rb') as grammar_file:
        grammar = pickle.load(grammar_file)
        print(grammar)

        for rule in grammar.rules:
            print(rule)
