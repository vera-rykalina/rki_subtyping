import pandas as pd
import sys
from textwrap import wrap

# Open .json file
infilename = sys.argv[1]
outfilename = sys.argv[2]

f = open(infilename, "rb")
df=pd.read_excel(f)
f.close()

name1 = infilename.rsplit("/")[-1]
name2 = name1.split("_")[-1].split(".")[-2] # get fragment part
name3 = name1.split(".")[-2] # cut xlsx

names = []
sequences = []

for i, row in df.iterrows():
    if row[name2 + "_Subtype"] == "Manual":
        names.append(row["SequenceName"])
        sequences.append(row["Sequenz"])



# Write into a fasta file
with open(name3 + ".fasta", "w") as file:
    for i in range(len(names)):
        file.writelines(">" + names[i])
        file.writelines("\n")
        file.writelines("\n".join(wrap(sequences[i], 60)))
        file.writelines("\n")