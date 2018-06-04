# 96 quite bitter beings

import pickle, argparse
from grammar import dd, Node, Rule, Grammar, PICKLE_FILE

def print_table(table: list):
    for i, lst in enumerate(table):
        for j, cell in enumerate(lst):
            if i <= j:
                print("{:>2} {:>2}".format(i, j), cell)

def visit(words, table, i, j, k, idx, indent=0):
    next_pos = table[i][j][idx]

    if len(next_pos) == 1:
        print(" " * indent, next_pos[0], words[i])
        return
    else:
        print(" " * indent, next_pos[0])

    lhs, k, left_idx, right_idx = next_pos
    visit(words, table, i, k, k, left_idx, indent + 2)
    visit(words, table, k + 1, j, k, right_idx, indent + 2)

def cky_parse(grammar: Grammar, sentence: list) -> list:
    table = []
    words = sentence.split()
    for i in range(len(words)):
        table.append([[] for _ in range(len(words))])

    for j, word in enumerate(words):
        # fill [j, j] cell with rule -> word
        for rule in grammar.words_pos[word]:
            table[j][j].append(("{}_NT".format(rule),))

        for rule in grammar.rules:
            # "flatten" unit productions
            if len(rule.rhs) == 1 and \
                rule.rhs[0] in [pos[0] for pos in table[j][j]]:
                unit_str = "{}->{}".format(rule.lhs, rule.rhs[0])
                table[j][j].append((unit_str,))

        # fill [j, (i: j..0)] (upwards)
        for i in reversed(range(j)):
            for k in range(i, j):
                # print("{}-{}: {}-{} + {}-{}".format(i, j, i, k, k + 1, j))
                # print(table[i][k], table[k + 1][j])
                for rule in grammar.rules:
                    if len(rule.rhs) == 2 and \
                       rule.rhs[0] in [pos[0].split("->")[0] for pos in table[i][k]] and \
                       rule.rhs[1] in [pos[0].split("->")[0] for pos in table[k + 1][j]]:
                        idx1 = [pos[0].split("->")[0] for pos in table[i][k]].index(rule.rhs[0])
                        idx2 = [pos[0].split("->")[0] for pos in table[k + 1][j]].index(rule.rhs[1])
                        table[i][j].append((rule.lhs, k, idx1, idx2))

    if 'S' in [rules[0] for rules in table[0][len(words) - 1]]:
        sentences = filter(lambda r: r[0] == 'S', table[0][len(words) - 1])
        for sentence in sentences:
            lhs, k, left_idx, right_idx = sentence
            visit(words, table, 0, len(words) - 1, k, left_idx, indent=0)
            print("---")

def pcky_parse(grammar: Grammar, sentence: list) -> list:
    table = []
    words = sentence.split()
    for i in range(len(words)):
        table.append([[] for _ in range(len(words))])

    for j, word in enumerate(words):
        # fill [j, j] cell with rule -> word
        for rule in grammar.words_pos[word]:
            table[j][j].append(("{}_NT".format(rule),))

        for rule in grammar.rules:
            # "flatten" unit productions
            if len(rule.rhs) == 1 and \
                rule.rhs[0] in [pos[0] for pos in table[j][j]]:
                unit_str = "{}->{}".format(rule.lhs, rule.rhs[0])
                table[j][j].append((unit_str,))

        # fill [j, (i: j..0)] (upwards)
        for i in reversed(range(j)):
            for k in range(i, j):
                # print("{}-{}: {}-{} + {}-{}".format(i, j, i, k, k + 1, j))
                # print(table[i][k], table[k + 1][j])
                for rule in grammar.rules:
                    if len(rule.rhs) == 2 and \
                       rule.rhs[0] in [pos[0].split("->")[0] for pos in table[i][k]] and \
                       rule.rhs[1] in [pos[0].split("->")[0] for pos in table[k + 1][j]]:
                        idx1 = [pos[0].split("->")[0] for pos in table[i][k]].index(rule.rhs[0])
                        idx2 = [pos[0].split("->")[0] for pos in table[k + 1][j]].index(rule.rhs[1])
                        table[i][j].append((rule.lhs, k, idx1, idx2))

    if 'S' in [rules[0] for rules in table[0][len(words) - 1]]:
        sentences = filter(lambda r: r[0] == 'S', table[0][len(words) - 1])
        for sentence in sentences:
            lhs, k, left_idx, right_idx = sentence
            visit(words, table, 0, len(words) - 1, k, left_idx, indent=0)
            print("---")

if __name__ == "__main__":
    with open(PICKLE_FILE, 'rb') as grammar_file:
        grammar = pickle.load(grammar_file)
        sentence = "This is really rewarding ."

        argparser = argparse.ArgumentParser(description="Grammar extractor")
        argparser.add_argument("sentence", help="Sentence to be parsed")
        argparser.add_argument(
            '-p',
            '--probabilistic',
            help="Probabilistic CKY",
            action='store_true')

        args = argparser.parse_args()

        if args.probabilistic:
            pcky_parse(grammar, args.sentence)
        else:
            cky_parse(grammar, args.sentence)
