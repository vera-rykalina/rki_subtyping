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
name3 = name1.split("20M")[-2]


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


# Iterate over rows in df (some sequences may have NAs as a subtype)
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
df.drop("Subtype%", axis=1, inplace = True)

# Replace subsubtypes (e.g. A2 -> A, F1 -> F)
df["Stanford_" + name2 + "_Subtype"] = df["Stanford_" + name2 + "_Subtype"].replace(r"^(\w{1})\d{1}$", r"\1", regex=True)

# Check output
print(df.head())
print(df.tail())

# Sort df by SequenceName
df = df.sort_values(by=["SequenceName"])

# Convert a pandas dataframe to a .csv file
df.to_csv("stanford_" + name3 + "20M.csv", index=False, sep=",", encoding="utf-8")

