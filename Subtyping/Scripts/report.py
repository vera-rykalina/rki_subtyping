#!/bin/python3

# Import libraries
import pandas as pd


# Read .csv file
df_full_prrt = pd.read_excel("full_PRRT.xlsx")
df_full_env = pd.read_excel("full_ENV.xlsx")
df_full_int = pd.read_excel("full_INT.xlsx")

# Prepare final report
final_report = df_full_prrt[["Scount", "PRRT_Subtype"]].copy()

# Rename two first columns 
final_report.rename(columns = {"Scount":"SCount", "PRRT_Subtype": "Subtyp_PRRT"}, inplace = True)

# Add other columns
final_report["Subtyp_INT"] = df_full_int["INT_Subtype"].copy()
final_report["Subtyp_ENV"] = df_full_env["ENV_Subtype"].copy()
final_report["Subtyp_Summe"] = None
final_report["Env_FPR"] = None

# Make a decision
for i, row in final_report.iterrows():
    if row["Subtyp_PRRT"] == row["Subtyp_INT"] and row["Subtyp_PRRT"] == row["Subtyp_ENV"]:
        final_report.at[i, ["Subtyp_Summe"]] = row["Subtyp_PRRT"]
    elif row["Subtyp_PRRT"] == "_Seq. nicht klassifizierbar" or row["Subtyp_INT"] == "_Seq. nicht klassifizierbar":
        final_report.at[i, ["Subtyp_Summe"]] = "_Seq. nicht klassifizierbar"
    else:
        final_report.at[i, ["Subtyp_Summe"]] = "Manual"


final_report.to_excel("_subtype_uploads.xlsx", index=False, encoding="utf-8")