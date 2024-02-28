#!/usr/bin/env python3

# Import libraries
import json
import pandas as pd
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


for infilename in sys.argv[1:]:
    name0 = infilename.rsplit("/")[-1] # gives a file name.csv
    list_of_substrings = name0.split("_")
    # Initiate lists and dictionary
    columns = {}
    col_header = []
    col_subtype = []
    if "PRRT" in list_of_substrings or "INT" in list_of_substrings:
        # Extract useful info 
        for sequence in data: 
            col_header.append(sequence["inputSequence"]["header"])
            col_subtype.append(sequence["subtypeText"])
        # Add info to the dictionary
        columns["SequenceName"] = col_header
        columns["Subtype%"] = col_subtype
        # Create a dataframe
        df = pd.DataFrame(columns)

    if "ENV" in list_of_substrings:
        # Extract useful info 
        for sequence in data: 
            col_header.append(sequence["inputSequence"]["header"])
            col_subtype.append("NA")
        # Add info to the dictionary
        columns["SequenceName"] = col_header
        columns["Subtype%"] = col_subtype
        # Create a dataframe
        df = pd.DataFrame(columns)


# Create new columns "Stanford_Fragment_Subtype" and "Stanford_Fragment_Comment"
# Split subtype and % components in Subtype%

df[["Stanford_" + name2 + "_Subtype", "Stanford_" + name2 + "_Comment"]] = df["Subtype%"].str.rsplit(" ", n=1, expand=True)
df["Stanford_" + name2 + "_Comment"] = df["Stanford_" + name2 + "_Comment"].fillna("No_value")
df["Stanford_" + name2 + "_Comment"] = df["Stanford_" + name2 + "_Comment"].replace("No_value", "(0.00%)")
df["Stanford_" + name2 + "_Subtype"] = df["Stanford_" + name2 + "_Subtype"].replace("Unknown", "Unassigned")
df["Stanford_" + name2 + "_Subtype"] = df["Stanford_" + name2 + "_Subtype"].replace("NA", "Unassigned")
df["Stanford_" + name2 + "_Subtype"] = df["Stanford_" + name2 + "_Subtype"].replace("", "Unassigned")
df["Stanford_" + name2 + "_Subtype"] = df["Stanford_" + name2 + "_Subtype"].replace(r"^(\w+)\s\+\s(\w+)\s\+\s(\w+)$", r"\1, \2, \3", regex=True)
df["Stanford_" + name2 + "_Subtype"] = df["Stanford_" + name2 + "_Subtype"].replace(r"^(\w+)\s\+\s(\w+)$", r"\1, \2", regex=True)

# Remove original subtype column as formatted: A (5.08%), it works in place
df.drop("Subtype%", axis=1, inplace = True)

# Sort df by SequenceName
df = df.sort_values(by=["SequenceName"])

# Convert a pandas dataframe to a .csv file
df.to_csv("stanford_" + name3 + ".csv", index=False, sep=",", encoding="utf-8")

