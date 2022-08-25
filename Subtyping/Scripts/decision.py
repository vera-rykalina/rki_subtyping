#!/bin/python3

# Import libraries
import pandas as pd
import sys
import re


infilename = sys.argv[1]
outfilename = sys.argv[2]

# Read .csv file
f = open(infilename, "rb")
df = pd.read_csv(f, sep = ",")
f.close()

name1 = infilename.rsplit("/")[-1] # gives a file name.csv
name2 = name1.split("_")[-2] # gives a middle part after splitting by "_"
name3 = name1.split("joint_")[-1].split(".")[-2] # cuts .csv
print(name3)

# Create 'Scount' column in dfs
df["Scount"] = df["SequenceName"].str.extract("(^\d+-\d+)_\w{2,4}_\d+_?\w+?$", expand=True)

# Change the position of this column from last to first in all dfs
col1 = df.pop('Scount')
df.insert(0, 'Scount', col1)

# Change data type string -> float
df["Comet_" + name2 + "_Comment"] = pd.to_numeric(df["Comet_" + name2 + "_Comment"], downcast="float")


# Make a decision for PRRT and INT
if name2 == "PRRT" or "INT":
    for i, row in df.iterrows():
        if row["Stanford_" + name2 + "_Subtype"] == row["Comet_" + name2 + "_Subtype"] and row["Comet_" + name2 + "_Comment"] >= 50:
            df.at[i, [name2 + "_Subtype"]] = row["Stanford_" + name2 + "_Subtype"]
        else:
            df.at[i, [name2 + "_Subtype"]] = "Manual" 

    # Prepare .csv file
    df.to_csv("decision_" + name3 + ".csv", sep=",", index=False, encoding="utf-8")



# Make a decision for ENV
if name2 == "ENV":
    for i, row in df.iterrows():
        if row["Rega_" + name2 + "_Subtype"][0] == row["Comet_" + name2 + "_Subtype"] and len(row["Rega_" + name2 + "_Subtype"]) < 3 and row["Comet_" + name2 + "_Comment"] >= 50:
            df.at[i, [name2 + "_Subtype"]] = row["Comet_" + name2 + "_Subtype"]

        elif row["Rega_" + name2 + "_Subtype"] != row["Comet_" + name2 + "_Subtype"] and row["Comet_" + name2 + "_Comment"] >= 70:
            df.at[i, [name2 + "_Subtype"]] = row["Comet_" + name2 + "_Subtype"]

        else:
            df.at[i, [name2 + "_Subtype"]] = "Manual"
    
    # Prepare .csv file
    df.to_csv("decision_" + name3 + ".csv", sep=",", index=False, encoding="utf-8")