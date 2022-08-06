#!/bin/python3

# Import libraries
import pandas as pd
import sys
import re
from Bio import SeqIO

infilename = sys.argv[1]
outfilename = sys.argv[2]

# Read fasta
names = []
sequences = []

fasta_sequences = SeqIO.parse(open(infilename),'fasta')
for fasta in fasta_sequences:
    names.append(fasta.id)
    sequences.append(str(fasta.seq))
print(names)
print(sequences)
print(len(sequences))     

from collections import Counter
counts = Counter(names)
for name, num in counts.items():
    print(name, num)
    if num > 1:
        for suffix in range(1, num + 1):
            if num == 1:
                names[names.index(name)] = name
            else: 
                names[names.index(name)] = name + 'R' 

print(names)
# name1 = infilename.rsplit("/")[-1] # gives a file name.fasta
# name2 = name1.split("_")[-2] # gives a middle part after splitting by "_"
# name3 = name1.split(".")[-2] # cuts .fasta


# with open(name3 + "R" + ".fasta", "w") as file:
#     file.writelines()