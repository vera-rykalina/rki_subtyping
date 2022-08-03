#!/bin/python3

# Import libraries
import pandas as pd
import sys
import re

infilename = sys.argv[1]
outfilename = sys.argv[2]

# Read .csv file
f = open(infilename, "rb")
df = pd.read_excel(f)
f.close()


name1 = infilename.rsplit("/")[-1] # gives a file name.csv
name2 = name1.split("_")[-3] # gives a middle part after splitting by "_"
name3 = name1.split(".")[-2] # cuts .xlsx


# Select only what is needed
df = df.loc[:,["Scount", "Header", "Sequenz"]]

#print(df)

df["SequenceName"] = df["Header"].str.extract("(\d\d-\d{5,6}_\w{2,4}_\d{2})_?\w{0,}?$", expand=True)
#print(df)
df[name2 + "_Subtype"] = df["Header"].str.extract("\d\d-\d{5,6}_\w{3,4}_\d{2}(_\w{0,}?)$")


# print(df)
# #df["SeqInfo"] = df["SeqInfo"].fillna(df["SequenceNumber"])
# df_joint = pd.read_csv("/Users/vera/Learning/CQ/Internship/rki_subtyping_resistance/Subtyping/Results/joint_fragmentwise/ENV_joint.csv", sep = ",")
# df_joint["ENV_Subtype"] = None
# df_joint["ENV_Subtype"] = df_joint["ENV_Subtype"].fillna(df["ENV_Subtype"])
# print(df_joint.head(20))

# Sort df by SequenceName
df = df.sort_values(by=["SequenceName"])


# Prepare a clean .csv file
df.to_csv("tagged_" + name3 + ".csv", sep=",", index=False, encoding="utf-8")
