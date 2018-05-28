# 96 quite bitter beings

import pickle
from grammar import dd, Node, Rule, Grammar, PICKLE_FILE

def print_table(table: list):
    for lst in table:
        print(lst)

def cky_parse(grammar: Grammar, sentence: list) -> list:
    table = []
    for i in range(len(sentence.split())):
        table.append([[] for _ in range(i + 1)])
    print(table)

    words = sentence.split()
    for j, word in enumerate(words, start=1):
        print(word)
        for rule in grammar.words_pos[word]:
            print(rule)
            table[j - 1][j - 1].append(rule)
        print_table(table)
        print("---")

        print(list(reversed(range(j))))
        for i in reversed(range(j)):

            for k in range(i, j):
                print(i, k)
                #for rules -> BC:
                #    if B in table[i][k - 1] and C in table[k][j - 1]:
                #        table[i][j - 1].append(rule)

if __name__ == "__main__":
    with open(PICKLE_FILE, 'rb') as grammar_file:
        grammar = pickle.load(grammar_file)
        sentence = "The man jumps"

        cky_parse(grammar, sentence)
