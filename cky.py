# 96 quite bitter beings

from grammar import Grammar

table = []
words = "Book the flight to Houston"
for i in range(len(words.split())):
    table.append([[] for _ in range(i + 1)])
print(table)

def cky_parse(grammar: Grammar, words: list) -> list:
    pass

# for j in len(words):
#     for all rules that make this word:
#         table[j - 1][j] = table[j - 1][j] union rule
#     for i in reversed(range(j - 2)):
#         for k in range(i + 1, j -1):
#             for all rules that make BC and B in table[i, k] and C in table[k, j]:
#                 table[i, j] = table[i, j] union rule
