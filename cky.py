# 96 quite bitter beings

import pickle
from grammar import dd, Node, Rule, Grammar, PICKLE_FILE

def print_table(table: list):
    for idx, lst in enumerate(table):
        print("{:>2}".format(idx), lst)

def cky_parse(grammar: Grammar, sentence: list) -> list:
    table = []
    words = sentence.split()
    for i in range(len(words)):
        table.append([set() for _ in range(len(words))])

    for j, word in enumerate(words):
        print(j, word)

        # fill [j, j] cell with RULE -> word
        for rule in grammar.words_pos[word]:
            print(rule)
            table[j][j].add("{}_NT".format(rule))
        print_table(table)
        print("---")

        # fill [j, (i: j..0)] (upwards)
        print("rev", list(reversed(range(j))))
        for i in reversed(range(j)):
            for k in range(i, j):
                for rule in grammar.rules:
                    if len(rule.rhs) == 2 and \
                       rule.rhs[0] in table[i][k] and \
                       rule.rhs[1] in table[k + 1][j]:
                        table[i][j].add(rule.lhs)

    print_table(table)

if __name__ == "__main__":
    with open(PICKLE_FILE, 'rb') as grammar_file:
        grammar = pickle.load(grammar_file)
        sentence = "Have they been practicing lately ?"

        cky_parse(grammar, sentence)
