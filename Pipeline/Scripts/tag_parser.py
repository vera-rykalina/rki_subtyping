# Import libraries
import pandas as pd
import sys
import re
from collections import Counter

infilename = sys.argv[1]
outfilename = sys.argv[2]

# Read .xlsx file
f = open(infilename, "rb")
df = pd.read_excel(f)
f.close()


name1 = infilename.rsplit("/")[-1] # gives a file name.csv
name2 = name1.split("_")[-3] # gives a middle part after splitting by "_"
name3 = name1.split("_")[0] # get run index


# Select only what is needed
df = df.loc[:,["Scount", "Header", "Sequenz"]]


df["SequenceName"] = df["Header"].str.extract("(^\d\d-\d{5,6}_\w{2,4}_\d{2})_?\w{0,}?$", expand=True)

df[name2 + "_Info"] = df["Header"].str.extract("^\d\d-\d{5,6}_\w{2,4}_\d{2}(_\w{0,}?)$")


seq_names = list(df["SequenceName"])


# Mark repeats
counts = Counter(seq_names)
for name, num in counts.items():
    if num > 1:
        for suffix in range(1, num+1):
            seq_names[seq_names.index(name)] = name + "repeat" + str(suffix)

df_marked = pd.DataFrame({'Marked': seq_names})


df["SequenceName"] = df_marked["Marked"]


# Select only what is needed
df = df.loc[:,["SequenceName", "Sequenz", name2 + "_Info"]]

# Rename Sequenz to Sequence
df.rename(columns={"Sequenz": "Sequence"}, inplace=True)

# Sort df by Scount
df = df.sort_values(by=["SequenceName"])


# Create "Repeat" columns
df["Repeat"] = df["SequenceName"].str.extract("^\d+-\d+_\w{2,4}_\d+(repeat\d{1})?$", expand=True)


# Prepare a clean .csv file
df.to_csv("tag_" + name3 + "_" + name2 + "_20M" + ".csv", sep=",", index=False, encoding="utf-8")
