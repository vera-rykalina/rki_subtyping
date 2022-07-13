#!/bin/python3

# Import libraries
import json
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
columns["SCount"] = col_header
columns["Subtype%"] = col_subtype

# Create a dataframe
df = pd.DataFrame(columns)

# Split subtype and % components of the string
# Create a new columns "Comment"
# str.rstrip - splits a string by a separator, starting from the right
df[["Subtype", "Comment"]] = df["Subtype%"].str.rsplit(" ", n=1, expand=True)


# Remove original subtype column as formatted: A (5.08%)
df = df.drop(columns=["Subtype%"])

# Check output
print(df.head())
print(df.tail())


# Convert a pandas dataframe to .csv file
df.to_csv("MS95_PRRT_20.csv",index=False, sep=",", encoding='utf-8')
