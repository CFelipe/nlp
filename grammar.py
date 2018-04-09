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

def print_tree(node, level = 0):
    """Prints a tree in pre-order"""

    if node is not None:
        print("| " * level + node.root)
        for n in node.children:
            print_tree(n, level + 1)

def save_rule(node, rules):
    """Saves grammar rules"""

    if node is not None:
        if node.children:
            formatted_children = " ".join([node.root for node in node.children])
            # print("{} -> {}".format(node.root, formatted_children))
            rules.append("{} -> {}".format(node.root, formatted_children))

        for n in node.children:
            save_rule(n, rules)

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

        print(len(rules))
        print(Counter(rules).most_common(30))

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Grammar extractor")
    argparser.add_argument("input_file", help="Corpus file")
    args = argparser.parse_args()
    extract_grammar(args.input_file)
