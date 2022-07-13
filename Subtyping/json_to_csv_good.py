#!/bin/python3

# Import libraries
import json
import pandas as pd

# Open JSON file
with open("baker.json") as f:
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

# Split subtype and % components of the string
# Create a new columns "Comment"
# str.rstrip - splits string around given separator, starting from the right
df[["Subtype", "Comment"]] = df["Subtype%"].str.rsplit(" ", n=1, expand=True)


# Remove original subtype column <A (5.08%)>
df = df.drop(columns=["Subtype%"])

# Check output
print(df.head())
print(df.tail())


# Convert a plsandas dataframe to .csv file
df.to_csv("stanford_PRRT.csv",index=False, sep=",", encoding='utf-8')
