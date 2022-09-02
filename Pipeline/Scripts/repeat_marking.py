# Import libraries
import sys
from Bio import SeqIO
from collections import Counter
from textwrap import wrap

infilename = sys.argv[1]
outfilename = sys.argv[2]

# Parse fasta
names = []
sequences = []
fasta_sequences = SeqIO.parse(open(infilename),'fasta')
for fasta in fasta_sequences:
    names.append(fasta.id.split("_badAlign")[0])
    sequences.append(str(fasta.seq))

# Mark repeats
counts = Counter(names)
for name, num in counts.items():
    if num > 1:
        for suffix in range(1, num+1):
            names[names.index(name)] = name + "repeat" + str(suffix)



name1 = infilename.rsplit("/")[-1] # gives a file name.fasta
name2 = name1.split("_")[-2] # gives a middle part after splitting by "_"
name3 = name1.split(".")[-2] # cuts .fasta


# Write into a file after marking repeated samples
with open(name3 + "M" + ".fasta", "w") as file:
    for i in range(len(names)):
        file.writelines(">" + names[i])
        file.writelines("\n")
        file.writelines("\n".join(wrap(sequences[i], 60)))
        file.writelines("\n")


