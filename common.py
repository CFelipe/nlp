import sys
import pickle
from pathlib import Path

def tokenize(chars: str) -> list:
    "Convert a string of characters into a list of tokens."
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()

class Tagger:
    def __init__(self):
        p = Path("models")
        p.mkdir(parents=True, exist_ok=True)

    def train(self):
        raise NotImplementedError()

    def load_model(self) -> None:
        try:
            with open(self.PICKLE_FILE, 'rb') as input_file:
                self.model = pickle.load(input_file)
        except OSError:
            print("Model not found")
            sys.exit(0)


    def tag_sentence(self, sentence: str) -> None:
        raise NotImplementedError()

    def tag_file(self, input_filename: str) -> None:
        with open(input_filename, 'r') as sentences_file:
            with open(input_filename + ".tst", 'w') as output_file:
                for sentence in sentences_file:
                    output_file.write(tag_sentence(sentence) + "\n")
