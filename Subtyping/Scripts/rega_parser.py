#!/bin/python3

# Import libraries
import pandas as pd
import sys
import re

infilename = sys.argv[1]
outfilename = sys.argv[2]


# Read .csv file
f = open(infilename, "r")
df = pd.read_csv(f, sep = ";")
f.close()


name1 = infilename.rsplit("/")[-1] # gives a file name.csv
name2 = name1.split("_")[-2] # gives a middle part after splitting by "_"
name3 = name1.split("_rega_")[-1].split(".")[-2] # {run_index}_{framgment}_20M


# Select only what is needed
df = df.loc[:,["name", "assignment", "pure", "crf"]]


# Simple replacements
df[["pure", "assignment", "crf"]] = df[["pure", "assignment", "crf"]].replace(r"^Check the report$", r"ChkRep", regex=True)

df[["pure", "assignment", "crf"]] = df[["pure", "assignment", "crf"]].replace(r"^HIV2 subtype A$", r"HIV2-A", regex=True)

df[["pure", "assignment", "crf"]] = df[["pure", "assignment", "crf"]].replace(r"^Recombinant$", r"URF", regex=True)

# HIV 1 N group -> Gruppe N
df[["pure", "assignment", "crf"]] = df[["pure", "assignment", "crf"]].replace(r"^HIV\s1\s(\w)\sgroup$", r"Gruppe \1", regex=True)



# "HIV-1 SUBTYPE" group

# HIV-1 Subtype A -> A
df[["pure", "assignment", "crf"]] = df[["pure", "assignment", "crf"]].replace(r"^\w{3}-\d\s\w{7}\s(\w)$", r"\1", regex=True)

# HIV-1 Subtype A (A1) -> A1
df[["pure", "assignment", "crf"]] = df[["pure", "assignment", "crf"]].replace(r"^\w{3}-\d\s\w{7}\s\w\s\((\w\d)\)$", r"\1", regex=True)

# HIV-1 Subtype A (01_AE) -> A 01_AE
df[["pure", "assignment", "crf"]] = df[["pure", "assignment", "crf"]].replace(r"^\w{3}-\d\s\w{7}\s(\w\s\(\d{2}_\w{2}\))$", r"\1", regex=True)

# HIV-1 Subtype A (06_CPX) -> A (06_cpx)
df[["pure", "assignment", "crf"]] = df[["pure", "assignment", "crf"]].replace(r"^HIV-1\sSubtype\s(\w\s\(\d{2}_CPX\))$", r"\1", regex=True)

# "HIV-1 CRF" group
# HIV-1 CRF 14_BG -> CRF14_BG
df[["pure", "assignment", "crf"]] = df[["pure", "assignment", "crf"]].replace(r"^HIV-1\sCRF\s(\d{2}_\w{2})$", r"CRF\1", regex=True)

# HIV-1 CRF 11_CPX -> CRF11_cpx
df[["pure", "assignment", "crf"]] = df[["pure", "assignment", "crf"]].replace(r"^HIV-1\sCRF\s(\d{2})_CPX$", r"CRF\1_cpx", regex=True)

# HIV-1 CRF 25_cpx -> CRF25_cpx
df[["pure", "assignment", "crf"]] = df[["pure", "assignment", "crf"]].replace(r"^HIV-1\sCRF\s(\d{2})_cpx$", r"CRF\1_cpx", regex=True)

# HIV-1 CRF 43_02G or HIV-1 CRF 22_02A1 -> CRF43_02G or CRF22_01A1
df[["pure", "assignment", "crf"]] = df[["pure", "assignment", "crf"]].replace(r"^HIV-1\sCRF\s(\d{2}_\d{2}\w\d?)$", r"CRF\1_cpx", regex=True)

# "LIKE" group (below are some examples)

# HIV-1 Subtype G-like -> G-like
# HIV-1 Subtype A (A1)-like -> A (A1)-like
df[["pure", "assignment", "crf"]] = df[["pure", "assignment", "crf"]].replace(r"^HIV-1\sSubtype\s(\w{1,}\s?\(?\w?\d?\)?-like)$", r"\1", regex=True)

# HIV-1 CRF 01_AE-like -> 01_AE-like
df[["pure", "assignment", "crf"]] = df[["pure", "assignment", "crf"]].replace(r"^HIV-1\sCRF\s(\w{1,}-like)$", r"\1", regex=True)

# POTENTIAL RECOMBINANT group (below are some examples)
# HIV-1 Subtype B, potential recombinant -> potReCo(B)
# HIV-1 Subtype A (A1), potential recombinant -> potReCo(A)
df[["pure", "assignment", "crf"]] = df[["pure", "assignment", "crf"]].replace(r"^HIV-1\sSubtype\s(\w)\s?\(?\w?\d?\)?,\spotential\srecombinant$", r"potReCo(\1)", regex=True)

# RECOMBINANT OF group (below are some examples)
# Recombinant of A1, B or Recombinant of B -> ReCo(B,F1)
# Recombinant of A1, B, D or Recombinant of B, A1, G -> ReCo(A1,B,D)
# Recombinant of A1, 03_AB -> ReCo(A1,03_AB)
# Recombinant of B, 39_BF, D -> ReCo(B,39_BF,D)
df[["pure", "assignment", "crf"]] = df[["pure", "assignment", "crf"]].replace(r"^Recombinant\sof\s(\w{0,}\d?,?)\s?(\w{0,}\d?,?)\s?(\w{0,}\d?)$", r"ReCo(\1\2\3)", regex=True)


# Fill nan objects with "-"
df[["pure", "assignment", "crf"]] = df[["pure", "assignment", "crf"]].fillna("-")


# Rename some columns (as done for stanford df)
df. rename(columns = {"name":"SequenceName", "assignment": "Rega_" + name2 + "_Subtype"}, inplace = True)

df["Rega_" + name2 + "_Comment"] = df["pure"].astype(str).str.strip() + " / " + df["crf"].astype(str).str.strip()


# Delete undesired columns
df.drop(columns=["pure", "crf"], axis = 1,  inplace = True)

# Sort df by SequenceName
df = df.sort_values(by=["SequenceName"])


# Prepare a clean .csv file
df.to_csv("rega_" + name3 + ".csv", sep=",", index=False, encoding="utf-8")

