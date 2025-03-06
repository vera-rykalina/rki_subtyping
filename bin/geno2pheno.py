#!/usr/bin/env python3

# Import libraries
import pandas as pd
import sys
import re

infilename = sys.argv[1]
outfilename = sys.argv[2]


# Read .csv file
f = open(infilename, "r")
df = pd.read_csv(f, sep = ",")
f.close()


name1 = infilename.rsplit("/")[-1] # gives a file name.csv
name2 = name1.split("_")[-2] # gives a middle part after splitting by "_"
name3 = name1.split("_Geno2Pheno_")[-1].split(".")[-2] # {run_index}_{fragment}_20M

# Select only what is needed
df = df.loc[:,["Sample", "Subtypes(Probability)"]]

# Rename columns (as done for stanford df)
df["Geno2Pheno_" + name2 + "_Subtype"] = df["Subtypes(Probability)"]
df["Geno2Pheno_" + name2 + "_Comment"] = df["Subtypes(Probability)"]

# Prepate a Subtype column
df["Geno2Pheno_" + name2 + "_Subtype"] = df["Geno2Pheno_" + name2 + "_Subtype"].str.replace(r"\(\d+[.,]?\d+\)|\(1\)", "", regex=True)
df["Geno2Pheno_" + name2 + "_Subtype"] = df["Geno2Pheno_" + name2 + "_Subtype"].str.replace(r",", ", ", regex=True)

                                                                        
# Prepate an Comment column
df["Geno2Pheno_" + name2 + "_Comment"] = df["Geno2Pheno_" + name2 + "_Comment"].str.replace(r"[A-Z]+\d+|[A-Z]+", r"", regex=True)
df["Geno2Pheno_" + name2 + "_Comment"] = df["Geno2Pheno_" + name2 + "_Comment"].str.replace(r",", r", ", regex=True)


# Replace AE to CRF01_AE
df["Geno2Pheno_" + name2 + "_Subtype"] = df["Geno2Pheno_" + name2 + "_Subtype"].str.replace(r"(.*)?(AE)(.*)?", r"\1CRF01_\2\3", regex = True)
#df["Geno2Pheno_" + name2 + "_Comment"] = df["Geno2Pheno_" + name2 + "_Comment"].str.replace(r"(.*)?(AE)(.*)?", r"\1CRF01_\2\3", regex = True)

# Rename Sample column (as done for stanford df)
df. rename(columns = {"Sample":"SequenceName"}, inplace = True)


# Remove tags from SequenceName column (_badAlign, _lowTrust, etc)
df["SequenceName"]= df["SequenceName"].str.extract(r"(\d{2}-\d{5}_\w{2,4}_20)", expand=True)

# Delete undesired columns
df.drop(columns=["Subtypes(Probability)"], axis = 1,  inplace = True)

# Prepare a clean .csv file
df.to_csv("g2p_" + name3 + ".csv", sep=",", index=False, encoding="utf-8")

