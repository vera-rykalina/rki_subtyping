#!/bin/python3

"""
To play with this parser outside of pipeline
python3 stanford_parser.py results/MS95_PRRT_20.json MS95_PRRT_20.csv
"""


# Import libraries
import json, os
import pandas as pd
import os
import sys


# Open .json file
infilename = sys.argv[1]
outfilename = sys.argv[2]

f = open(infilename, "r")
data=json.load(f)
f.close()

name1 = infilename.rsplit("/")[-1]
name2 = name1.split("_")[-2]
name3 = name1.split(".")[-2]


# Initiate lists and dictionary
columns = {}
col_header = []
col_subtype = []

# Extract useful info
for sequence in data:
    col_header.append(sequence["inputSequence"]["header"])
    col_subtype.append(sequence["subtypeText"])

# Add info to the dictionary
columns["SequenceName"] = col_header
columns["Subtype%"] = col_subtype

# Create a dataframe
df = pd.DataFrame(columns)


# Iterate over row in df (some sequence may have NAs as subtype)
# Create new columns "Subtype" and "Comment"

for i, row in df.iterrows():
    if row["Subtype%"] == "NA":
        df.at[i, ["Stanford_" + name2 + "_Subtype", "Stanford_" + name2 + "_Comment"]] = "NA"

    else:
        # split subtype and % components in the string
        # str.rstrip - splits a string by a separator, starting from the right
        df[["Stanford_" + name2 + "_Subtype", "Stanford_" + name2 + "_Comment"]] = df["Subtype%"].str.rsplit(" ", n=1, expand=True)


df["Stanford_" + name2 + "_Comment"] = df["Stanford_" + name2 + "_Comment"].fillna("NA")



# Remove original subtype column as formatted: A (5.08%), it works in place
#df.drop(columns=["Subtype%"], inplace = True)
df.drop("Subtype%", axis=1, inplace = True)

# Check output
print(df.head())
print(df.tail())

# Sort df by SequenceName
df = df.sort_values(by=["SequenceName"])

# Convert a pandas dataframe to a .csv file
df.to_csv("stanford_" + name3 + ".csv", index=False, sep=",", encoding="utf-8")


# Remove .json file
os.remove(infilename)
