#!/bin/python3

# Import libraries
import json, os, glob2
import pandas as pd
import os


# Open JSON file
for file in glob2.glob("/Users/vera/Learning/CQ/Internship/rki_subtyping_resistance/Subtyping/results/*.json"):
    with open(file) as f:
        data = json.load(f)
    name1 = file.rsplit("/")[-1]
    name2 = name1.split("_")[1]
    name3 = name1.rsplit(".")[-2] # gives a file name (cuts .json)
 

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
        df.at[i, ["Stanford_" + name2 + "_Subtype", "Stanford_" + name2 + "_Comment"]] = "NA"
    
    else:
        # split subtype and % components in the string
        # str.rstrip - splits a string by a separator, starting from the right
        df[["Stanford_" + name2 + "_Subtype", "Stanford_" + name2 + "_Comment"]] = df["Subtype%"].str.rsplit(" ", n=1, expand=True)


df["Stanford_" + name2 + "_Comment"] = df["Stanford_" + name2 + "_Comment"].fillna("NA")


# Check that type of "Comment" is a string now
#print(type(df.loc[0,"Comment"]))


# Remove original subtype column as formatted: A (5.08%), it works in place
#df.drop(columns=["Subtype%"], inplace = True)
df.drop("Subtype%", axis=1, inplace = True)

# Check output
print(df.head())
#print(df.tail())


# Convert a pandas dataframe to a .csv file
df.to_csv("stanford_" + name3 + ".csv", index=False, sep=",", encoding="utf-8")



for file in glob2.glob("/Users/vera/Learning/CQ/Internship/rki_subtyping_resistance/Subtyping/results/*.json"):
    os.remove(file)