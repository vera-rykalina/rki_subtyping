#!/bin/python3

# Import libraries
import json, os, glob2
import pandas as pd


# Open JSON file
for file in glob2.glob("/Users/vera/Learning/CQ/Internship/rki_subtyping_resistance/Subtyping/*/*.json"):
    with open(file) as f:
        data = json.load(f)



# Open JSON file
#file = "/Users/vera/Learning/CQ/Internship/rki_subtyping_resistance/Subtyping/results/prrt.json"
#with open(file) as f:
#    data = json.load(f)


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
        df.at[i, ["Stanford_PRRT_Subtype", "Stanford_PRRT_Comment"]] = "NA"
    
    else:
        # split subtype and % components in the string
        # str.rstrip - splits a string by a separator, starting from the right
        df[["Stanford_PRRT_Subtype", "Stanford_PRRT_Comment"]] = df["Subtype%"].str.rsplit(" ", n=1, expand=True)


df["Stanford_PRRT_Comment"] = df["Stanford_PRRT_Comment"].fillna("NA")


# Check that type of "Comments" is a string now
#print(type(df.loc[0,"Comment"]))


# Remove original subtype column as formatted: A (5.08%), it works in place
#df.drop(columns=["Subtype%"], inplace = True)
df.drop("Subtype%", axis=1, inplace = True)

# Check output
print(df.head())
#print(df.tail())


# Convert a pandas dataframe to a .csv file
df.to_csv("stanford_prrt.csv", index=False, sep=",", encoding="utf-8")

