import common
import argparse
import pickle
from collections import Counter
from pathlib import Path

PICKLE_FILE = "models/grammar-model.pkl"

class Node:
    def __init__(self, root: str, children: list = None):
        if children is None: children = []
        self.root = root
        self.children = children

    def __repr__(self):
        return "[R: {} + {} children]".format(self.root, len(self.children))


class Rule:
    def __init__(self, lhs: str, rhs: list):
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self):
        return "{:>10} -> {}".format(self.lhs, " ".join(self.rhs))

    def __eq__(self, other):
        return self.lhs == other.lhs and self.rhs == other.rhs

    def __hash__(self):
        return hash((tuple(self.lhs), tuple(self.rhs)))


# TODO: make terminals lowercase
class Grammar:
    def __init__(self, rules: list, terminals: set):
        self.rules = rules
        self.nonterminals = set()
        self.terminals = terminals

        for rule in self.rules:
            self.nonterminals.add(rule.lhs)

        assert self.terminals & self.nonterminals == set()

        self.cnf_term()
        self.cnf_bin()

    def cnf_term(self):
        term_rules = []
        for rule in self.rules:
            new_rhs = [
                "{}_NT".format(pos) if self.terminal(pos) else pos
                for pos in rule.rhs
            ]

            new_rule = Rule(rule.lhs, new_rhs)
            term_rules.append(new_rule)

        self.rules = term_rules

        # create nonterminal rules from terminals
        for terminal in self.terminals:
            nt_rule = Rule("{}_NT".format(terminal), [terminal])
            self.rules.append(nt_rule)

    def cnf_bin(self):
        new_rules = []
        for rule in self.rules:
            if len(rule.rhs) > 2:
                count = 0

                rhs = rule.rhs
                while len(rhs) > 2:
                    next_rule = "{}_{}".format(rule.lhs, count)
                    new_lhs = rule.lhs if count == 0 else next_rule
                    new_rhs = [rhs[0], "{}_{}".format(rule.lhs, count + 1)]
                    new_rules.append(Rule(new_lhs, new_rhs))
                    count += 1
                    rhs = rhs[1:]

                new_lhs = "{}_{}".format(rule.lhs, count)
                new_rhs = rhs
                new_rules.append(Rule(new_lhs, new_rhs))
            else:
                new_rules.append(rule)

        self.rules = new_rules

    def terminal(self, pos: str):
        return pos in self.terminals


def print_tree(node, level=0):
    """Prints a tree in pre-order"""

    if node is not None:
        print("| " * level + node.root)
        for n in node.children:
            print_tree(n, level + 1)


def save_rule(node, rules):
    """Saves grammar rules by adding nodes to the tree recursively"""

    if node:
        node.root = common.get_until_hyphen(node.root)

        if node.children and len(
                node.children) == 1 and node.children[0].root == "-NONE-":
            return
        elif node.children:
            node.children = [
                child for child in node.children if child.root != "-NONE-"
            ]

            rules.append(
                Rule(node.root, [child.root for child in node.children]))

            for n in node.children:
                save_rule(n, rules)


def extract_grammar(filename: str, args):
    with open(filename, "r") as corpus_file:
        pos_stack = []
        paren_stack = []
        prev = None
        root = None
        rules = []
        terminals = set()

        for line in corpus_file:
            tokens = common.tokenize(line)

            for token in tokens:
                if token == "(":
                    paren_stack.append("(")
                elif token == ")":
                    while True:
                        if not paren_stack:
                            return "bad"
                        else:
                            el = paren_stack.pop()
                            if pos_stack:
                                pos_stack.pop()
                            if el == "(":
                                break
                    if not paren_stack:
                        save_rule(root, rules)
                        pos_stack = []
                        paren_stack = []
                        prev = None
                        root = None
                else:
                    if prev == "(":
                        node = Node(token)
                        if pos_stack:
                            pos_stack[-1].children.append(node)
                        else:
                            root = node
                        pos_stack.append(node)
                    elif prev != "-NONE-":  # previous token was a POS, can only be a terminal
                        terminals.add(prev)

                prev = token

        MOST_COMMON_COUNT = 1000
        sorted_rules = Counter(rules).most_common()

        if args.mode == "pre":
            print("{:>5} | {}".format("count", "rule"))
            for rule in sorted_rules[:MOST_COMMON_COUNT]:
                print("{:>5} | {}".format(rule[1], rule[0]))

            sum_first = sum([rule[1] for rule in sorted_rules[:MOST_COMMON_COUNT]])
            sum_rest = sum([rule[1] for rule in sorted_rules[MOST_COMMON_COUNT:]])

            print("{} rules total:".format(len(rules)))
            print("{:>8} (first {})".format(sum_first, MOST_COMMON_COUNT))
            print("{:>8} (rest)".format(sum_rest))
            print("{:.3f}% coverage".format(100.0 * sum_first / len(rules)))
            assert len(rules) == sum_first + sum_rest
        else:
            grammar_rules = [rule[0] for rule in sorted_rules[:MOST_COMMON_COUNT]]
            grammar = Grammar(grammar_rules, terminals)
            for rule in grammar.rules:
                print(rule)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Grammar extractor")
    argparser.add_argument("input_file", help="Corpus file")
    argparser.add_argument(
        "-m",
        "--mode",
        choices=["pre", "post"],
        help="Rules pre or post CNF conversion",
        default="post")
    args = argparser.parse_args()
    grammar = extract_grammar(args.input_file, args)

    p = Path(PICKLE_FILE)
    with p.open('wb') as output_file:
        pickle.dump(grammar, output_file, pickle.HIGHEST_PROTOCOL)
