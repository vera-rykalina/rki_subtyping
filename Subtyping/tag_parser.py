#!/bin/python3

# Import libraries
import pandas as pd
import sys
import re

infilename = sys.argv[1]
#outfilename = sys.argv[2]


# Read .csv file
f = open(infilename, "rb")
df = pd.read_excel(f)
f.close()


name1 = infilename.rsplit("/")[-1] # gives a file name.csv
name2 = name1.split("_")[-3] # gives a middle part after splitting by "_"
name3 = name1.split(".")[-2] # cuts .xlsx


# Select only what is needed
df = df.loc[:,["Scount", "Header"]]

print(df)

df["SequenceNumber"] = df["Header"].str.extract("(\d\d-\d{5,6}_\w{3,4}_\d{2})_?\w{0,}?$", expand=True)
print(df)
df["SeqInfo"] = df["Header"].str.extract("\d\d-\d{5,6}_\w{3,4}_\d{2}(_\w{0,}?)$")
print(df)
df["SeqInfo"] = df["SeqInfo"].fillna(df["SequenceNumber"])
print(df)


# Simple replacements
# df[["pure", "assignment", "crf"]] = df[["pure", "assignment", "crf"]].replace(r"^Check the report$", r"ChkRep", regex=True)