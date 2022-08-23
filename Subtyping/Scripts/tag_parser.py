#!/bin/python3

# Import libraries
import pandas as pd
import sys
import re
from collections import Counter

infilename = sys.argv[1]
outfilename = sys.argv[2]

# Read .csv file
f = open(infilename, "rb")
df = pd.read_excel(f)
f.close()


name1 = infilename.rsplit("/")[-1] # gives a file name.csv
name2 = name1.split("_")[-3] # gives a middle part after splitting by "_"
name3 = name1.split(".")[-2] # cuts .xlsx


# Select only what is needed
df = df.loc[:,["Scount", "Header", "Sequenz"]]

#print(df)

df["SequenceName"] = df["Header"].str.extract("(\d\d-\d{5,6}_\w{2,4}_\d{2})_?\w{0,}?$", expand=True)
#print(df)
df[name2 + "_Info"] = df["Header"].str.extract("\d\d-\d{5,6}_\w{3,4}_\d{2}(_\w{0,}?)$")

for i, row in df.iterrows():
    if row[name2 + "_Info"] == "_badAlign":
        df.at[i, [name2 + "_Info"]] = None
    

seq_names = list(df["SequenceName"])
  

# Mark repeats
counts = Counter(seq_names)
for name, num in counts.items():
    if num > 1:
        for suffix in range(1, num+1):
            seq_names[seq_names.index(name)] = name + "repeat" + str(suffix)

df_marked = pd.DataFrame({'Marked': seq_names})


df["SequenceName"] = df_marked["Marked"]

# Sort df by Scount
df = df.sort_values(by=["Scount"])

# Select only what is needed
df = df.loc[:,["Scount", "Sequenz", name2 + "_Info"]]

# Prepare a clean .csv file
df.to_csv("tag_" + name3 + ".csv", sep=",", index=False, encoding="utf-8")
