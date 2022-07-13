"""
This script generates random sequences of length 1024.
I  used this sequneces to fill in the excel table to proceed with a
excel__to_fasta.py script.

"""

import random

nucleotides = ["A", "C", "G", "T"]
seq = ''

for i in range(1024):
    seq += random.choice(nucleotides)

print(len(seq))
print(seq)