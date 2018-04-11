import common
import argparse
from collections import Counter

class Node:
    def __init__(self, root, children=None):
        if children is None: children = []
        self.root = root
        self.children = children

    def __repr__(self):
        return "[R: {} + {} children]".format(self.root, len(self.children))

class Rule:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self):
        return "{:>10} -> {}".format(self.lhs, " ".join(self.rhs))

    def __eq__(self, other):
        return self.lhs == other.lhs and self.rhs == other.rhs

    def __hash__(self):
        return hash((tuple(self.lhs), tuple(self.rhs)))

def print_tree(node, level = 0):
    """Prints a tree in pre-order"""

    if node is not None:
        print("| " * level + node.root)
        for n in node.children:
            print_tree(n, level + 1)

def save_rule(node, rules):
    """Saves grammar rules"""

    if node:
        if node.children and len(node.children) == 1 and node.children[0].root == "-NONE-":
            return
        elif node.children:
            node.children = [child for child in node.children if child.root != "-NONE-"]
            rules.append(Rule(node.root, [child.root for child in node.children]))

            for n in node.children:
                save_rule(n, rules)

def cnf_binarize(rules):
    pass

def extract_grammar(filename: str):
    with open(filename, "r") as corpus_file:
        pos_stack = []
        paren_stack = []
        prev = None
        root = None
        rules = []

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
                prev = token

        MOST_COMMON_COUNT = 1000
        sorted_rules = Counter(rules).most_common()
        for rule in sorted_rules[:MOST_COMMON_COUNT]:
            print("{:>5} | {}".format(rule[1], rule[0]))

        sum_first = sum([rule[1] for rule in sorted_rules[:MOST_COMMON_COUNT]])
        sum_rest  = sum([rule[1] for rule in sorted_rules[MOST_COMMON_COUNT:]])

        print("{} rules total:".format(len(rules)))
        print("{:>8} (first {})".format(sum_first, MOST_COMMON_COUNT))
        print("{:>8} (rest)".format(sum_rest))
        print("{:.3f}% coverage".format(100.0 * sum_first / len(rules)))
        assert len(rules) == sum_first + sum_rest

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Grammar extractor")
    argparser.add_argument("input_file", help="Corpus file")
    args = argparser.parse_args()
    extract_grammar(args.input_file)
    # print(Rule("A", ["B C"]) == Rule("A", ["B C"]))
