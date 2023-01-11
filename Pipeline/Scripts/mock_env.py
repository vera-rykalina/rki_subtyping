# Import libraries
import pandas as pd
import sys
from textwrap import wrap

"""
This scritpt schould generate mock ENV .xlsx (for AllSeqCO20 folder) and .fasta (InputFasta) files, when ENV is not provided
"""

infilename = sys.argv[1]
outfilename = sys.argv[2]

# Read .xlsx file
f = open(infilename, "rb")
df_excel = pd.read_excel(f)
f.close()


name1 = infilename.rsplit("/")[-1] # gives a file name.csv
name2 = name1.split("_")[-3] # gives a middle part after splitting by "_"
name3 = name1.split("_")[0] # get run index


df_excel["Fragment"] = df_excel["Fragment"].replace(r"PRRT", r"ENV", regex = True)

env_sequence = "GGAATTAGACCAGTAGTGTCAACTCAACTGCTGTTAAATGGCAGTTTATCAGAAGAAGAAGAGGTAATAATTAGATCTGAAAATCTCACWGACAATGCTAAAACCATAATAGTGCAGCTGAAAGATCCTATAGAAATTAATTGTACAAGACCCAACAACAATACAAGAAAAAGTATACATATAGCACCAGGGAGAGCATTCTATGCAACAGGAGGCATAATAGGAAACATAAGACAAGCACATTGTAACCTTAGTGWAGTAAAATGGAATAATACTTTGCAAAAATTAGTTACAAAATTAAGAGAAAAATTTAATAATAAAACAATARAATTTCRACCACCCTCAGGAGGGGATCCAGAAATTGTAATGCATACTTTTAATTGTGGAGGGGAATTTTTCTACTGTAATACAACAAAGCTGTTTAACAGTACTTGGGATGGAAATGTAACTACATGGAATGATACAGGTAAAGATATCACACTCCCATGCAGAATAAAACAAATTGTAAACAGGTGGCAGGAAGTAGGAAAAG"

df_excel["Sequenz"] = env_sequence
df_excel["Header"] = df_excel["Header"].replace(r"(\d{2}-\d+)(_\w{2,4}_)(\d{2})(_\w+)?", r"\1_ENV_\3", regex = True)

print(df_excel.head())

# Create output file
df_excel.to_excel(name3 + "_Seqs_ENV_CO20_V5.xlsx", index=False, encoding="utf-8")



f = open(name3 + "_Seqs_ENV_CO20_V5.xlsx", "rb")
df_for_fasta = pd.read_excel(f)
f.close()

names = []
sequences = []


for i, row in df_for_fasta.iterrows():
    names.append(row["Header"])
    sequences.append(row["Sequenz"])

# Write into a fasta file
with open(name3 + "_ENV_20.fasta", "w") as file:
    for i in range(len(names)):
        file.writelines(">" + names[i])
        file.writelines("\n")
        file.writelines("\n".join(wrap(sequences[i], 60)))
        file.writelines("\n")
