#!/bin/python3

# Import libraries
import pandas as pd
import sys


infilename = sys.argv[1]
outfilename = sys.argv[2]



# Read .csv file
f = open(infilename, "r")
df = pd.read_csv(f, sep = ";")
f.close()


name1 = infilename.rsplit("/")[-1] # gives a file name.csv
name2 = name1.split("_")[-2] # gives a middle part after splitting by "_"
name3 = name1.rsplit(".")[-2] # gives a file name (cuts .csv)


#print(df.columns)
df = df.loc[:,["name", "assignment", "pure", "crf"]]


df["pure"] = df["pure"].astype(str).str.replace("HIV-1 Subtype", "")
df["assignment"] = df["assignment"].astype(str).str.replace("HIV-1 Subtype", "")
df["crf"] = df["crf"].astype(str).str.replace("HIV-1", "")
df["crf"] = df["crf"].astype(str).str.replace("Subtype", "")
# Rename some columns (as done for stanford df)
df. rename(columns = {"name":"SequenceName", "assignment": "Rega_" + name2 + "_Subtype"}, inplace = True)

df["Rega_" + name2 + "_Comment"] = df["pure"].astype(str).str.strip() + " / " + df["crf"].astype(str).str.strip()


# Delete undesired columns
df.drop(columns=["pure", "crf"], axis = 1,  inplace = True)

# Sort df by SequenceName
df = df.sort_values(by=["SequenceName"])


# Prepare a clean .csv file
df.to_csv("rega_" + name3 + ".csv", sep=",", index=False, encoding="utf-8")

#print(df)