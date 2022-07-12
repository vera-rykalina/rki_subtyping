import random

nucleotides = ["A", "C", "G", "T"]
seq = ''

for i in range(1024):
    seq += random.choice(nucleotides)

#seq = seq.

print(len(seq))
print(seq)