#!/usr/bin/env python3

# Import libraries
import pandas as pd
import sys
import re

# Read .csv file
for infilename in sys.argv[1:]:
    filename = infilename.rsplit("/")[-1] # gives a file name.csv
    list_of_substrings = filename.split("_")
    if "PRRT" in list_of_substrings:
        df_full_prrt = pd.read_excel(infilename)
    if "INT" in list_of_substrings:
        df_full_int = pd.read_excel(infilename)


outfilename = sys.argv[2]


# Select only what is needed
df_full_prrt = df_full_prrt.loc[:,["Scount", "PRRT_Subsubtype"]]
df_full_int = df_full_int.loc[:,["Scount", "INT_Subsubtype"]]


# Merge tables
final_report = df_full_prrt.merge(df_full_int, on = "Scount", how = "outer")

# Rename two first columns 
final_report.rename(columns = {"Scount":"SCount", "PRRT_Subsubtype": "Subtype_PRRT","INT_Subsubtype": "Subtype_INT"}, inplace = True)

# Initiate empty columns
final_report["Subtype_ENV"] = "_notSequenced"
final_report["Subtype"] = None

# Initiate special cases
special_cases = ["_noClassified",  "Manual", "_notSequenced"]


# Strip white space
final_report = final_report.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Make a decision
for i, row in final_report.iterrows():
    if row["Subtype_PRRT"] == row["Subtype_INT"]:
        final_report.at[i, ["Subtype"]] = row["Subtype_PRRT"]
    
    elif row["Subtype_PRRT"] not in special_cases and row["Subtype_INT"] in special_cases:
        final_report.at[i, ["Subtype"]] = row["Subtype_PRRT"]

    elif row["Subtype_INT"] not in special_cases and row["Subtype_PRRT"] in special_cases:
        final_report.at[i, ["Subtype"]] = row["Subtype_INT"]     
    
    else:
        final_report.at[i, ["Subtype"]] = "Manual"


# Sort df by SequenceName
final_report.sort_values(by=["SCount"], inplace=True)

# Create output file
datasetname = filename.split("_")[1]
final_report.to_excel(datasetname +"_report.xlsx", index=False, encoding="utf-8")