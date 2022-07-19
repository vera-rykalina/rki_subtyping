#!/bin/python3

# Import libraries
import json
import numpy as np
import pandas as pd

path = "/Users/vera/Learning/CQ/Internship/rki_subtyping_resistance/Subtyping/stanford/MS95_PRRT_20.json"


# Open JSON file
with open(path) as f:
    data = json.load(f)


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
        df.at[i, ["Subtype", "Comment"]] = "NA"
    
    else:
        # split subtype and % components in the string
        # str.rstrip - splits a string by a separator, starting from the right
        df[["Subtype", "Comment"]] = df["Subtype%"].str.rsplit(" ", n=1, expand=True)


df["Comment"] = df["Comment"].fillna("NA")


# Check that type of "Comments" is a string now
print(type(df.loc[0,"Comment"]))


# Remove original subtype column as formatted: A (5.08%), it works in place
#df.drop(columns=["Subtype%"], inplace = True)
df.drop("Subtype%", axis=1, inplace = True)

# Check output
print(df.head())
#print(df.tail())


# Convert a pandas dataframe to a .csv file
df.to_csv("stanford_prrt.csv", index=False, sep=",", encoding='utf-8')
