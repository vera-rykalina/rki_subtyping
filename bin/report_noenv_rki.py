#!/usr/bin/env python3

# Import libraries
import pandas as pd
import sys
import re

# Read .csv file
for infilename in sys.argv[1:]:
    name0 = infilename.rsplit("/")[-1] # gives a file name.csv
    list_of_substrings = name0.split("_")
    if "PRRT" in list_of_substrings:
        df_full_prrt = pd.read_excel(infilename)
    if "INT" in list_of_substrings:
        df_full_int = pd.read_excel(infilename)


outfilename = sys.argv[2]


# Select only what is needed
df_full_prrt = df_full_prrt.loc[:,["Scount", "PRRT_Subtype"]]
df_full_int = df_full_int.loc[:,["Scount", "INT_Subtype"]]



# Merge tables
final_report = df_full_prrt.merge(df_full_int, on = "Scount", how = "outer")

# Rename two first columns 
final_report.rename(columns = {"Scount":"SCount", "PRRT_Subtype": "Subtyp_PRRT","INT_Subtype": "Subtyp_INT"}, inplace = True)

final_report["Subtyp_ENV"] = "_nichtSequenziert"
final_report["Subtyp_Summe"] = None
final_report["Env_FPR"] = None


special_cases = ["_Seq. nicht klassifizierbar", "_Seq. nicht auswertbar", "_zu wenig PCR-Produkt", "Manual"]

# Replacements
final_report[["Subtyp_PRRT", "Subtyp_INT", "Subtyp_ENV"]] = final_report[["Subtyp_PRRT", "Subtyp_INT", "Subtyp_ENV"]].replace(r"^_notSequenced$", r"_zu wenig PCR-Produkt", regex=True)

final_report[["Subtyp_PRRT", "Subtyp_INT"]] = final_report[["Subtyp_PRRT", "Subtyp_INT"]].replace(r"^_SeqNichtAuswertbar$", r"_Seq. nicht auswertbar", regex=True)

final_report[["Subtyp_PRRT", "Subtyp_INT"]] = final_report[["Subtyp_PRRT", "Subtyp_INT"]].replace(r"^_nichtSequenziert$", r"_zu wenig PCR-Produkt", regex=True)

# Strip white space
final_report = final_report.applymap(lambda x: x.strip() if isinstance(x, str) else x)


# Make a decision
for i, row in final_report.iterrows():
    if row["Subtyp_PRRT"] == row["Subtyp_INT"]:
        final_report.at[i, ["Subtyp_Summe"]] = row["Subtyp_PRRT"]
    
    elif row["Subtyp_PRRT"] not in special_cases and row["Subtyp_INT"] in special_cases:
        final_report.at[i, ["Subtyp_Summe"]] = row["Subtyp_PRRT"]

    elif row["Subtyp_INT"] not in special_cases and row["Subtyp_PRRT"] in special_cases:
        final_report.at[i, ["Subtyp_Summe"]] = row["Subtyp_INT"]     
    
    elif row["Subtyp_INT"] != row["Subtyp_PRRT"] and len(row["Subtyp_INT"]) <=2 and len(row["Subtyp_PRRT"]) > 2 and row["Subtyp_PRRT"] not in special_cases:
        final_report.at[i, ["Subtyp_Summe"]] = row["Subtyp_PRRT"]
    
    elif row["Subtyp_INT"] != row["Subtyp_PRRT"] and len(row["Subtyp_PRRT"]) <=2 and len(row["Subtyp_INT"]) > 2 and row["Subtyp_INT"] not in special_cases:
        final_report.at[i, ["Subtyp_Summe"]] = row["Subtyp_PRRT"]

    else:
        final_report.at[i, ["Subtyp_Summe"]] = "Manual"


# Sort df by SequenceName
final_report.sort_values(by=["SCount"], inplace=True)

# Create output file
name1 = name0.split("_")[1]
final_report.to_excel(name1 + "_subtype_uploads.xlsx", index=False, encoding="utf-8")