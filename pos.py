import json
import pickle
import argparse
from naive import NaiveTagger
from viterbi import ViterbiTagger

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description='Parts-of-speech tagger')
    argparser.add_argument("-a", "--algorithm", help="Tagging algorithm", default="viterbi")
    arg_group = argparser.add_mutually_exclusive_group()
    arg_group.add_argument("-s", "--sentence",   help="Tag a sentence")
    arg_group.add_argument("-i", "--input_file", help="Input file")
    arg_group.add_argument("-t", "--train_file", help="Training file")
    args = argparser.parse_args()

    if args.algorithm == "viterbi":
        tagger = ViterbiTagger()
    elif args.algorithm == "naive":
        tagger = NaiveTagger()

    if args.input_file:
        tagger.tag_file(args.input_file)
    elif args.sentence:
        print(tagger.tag_sentence(args.sentence))
    elif args.train_file:
        tagger.train(args.train_file)
    else:
        argparser.print_help()

# python3 pos.py --train_file

# test with `evalb -p collins.prm gold.gld test.tst`
# test with `evalb -p collins.prm sentences23.gold sentences23.tst`
# tgrep:

# to generate a binary
# tgrep2 -p bank0.top bank0tgrep

# to search for TOP
# tgrep2 -c bank0tgrep -l TOP | less

# to search for VP, VPN etc (regex support)
# tgrep2 -c bank0tgrep -l /VP/ | less
# tgrep2 -c bank0tgrep -l /^VP/ | less
# tgrep2 -c bank0tgrep -l /^VP$/ | less

# dominates
# tgrep2 -c bank0tgrep -l '/^NP$/ < /PP/' | less

# directly dominates
# tgrep2 -c bank0tgrep -l '/^NP$/ << /PP/' | less
