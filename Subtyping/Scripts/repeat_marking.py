#!/bin/python3

# Import libraries
import sys
from Bio import SeqIO
from collections import Counter


infilename = sys.argv[1]
outfilename = sys.argv[2]

# Read fasta
names = []
sequences = []
fasta_sequences = SeqIO.parse(open(infilename),'fasta')
for fasta in fasta_sequences:
    names.append(fasta.id)
    sequences.append(str(fasta.seq))

# Mark repeats
counts = Counter(names)
for name, num in counts.items():
    if num > 1:
        for suffix in range(1, num+1):
            names[names.index(name)] = name + "repeat" + str(suffix)

# Create a new fasta file with marked samples
marked_fasta = ""
for i in range(len(names)):
    marked_fasta += f"{names[i]}\n{sequences[i]}\n"

print(marked_fasta)
name1 = infilename.rsplit("/")[-1] # gives a file name.fasta
name2 = name1.split("_")[-2] # gives a middle part after splitting by "_"
name3 = name1.split(".")[-2] # cuts .fasta



with open("../test/"+ name3 + ".fasta", "w") as file:
    file.writelines(marked_fasta)
