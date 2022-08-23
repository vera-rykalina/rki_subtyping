#!/bin/python3

# Import libraries
import pandas as pd
import sys
import re

# Read .csv file
df_prrt = pd.read_csv("joint_MS95_PRRT_20M.csv", sep = ",")
df_env = pd.read_csv("joint_MS95_ENV_20M.csv", sep = ",")
df_int = pd.read_csv("joint_MS95_INT_20M.csv", sep = ",")

# Create 'Scount' column in dfs
df_prrt["Scount"] = df_prrt["SequenceName"].str.extract("(^\d+-\d+)_\w{2,4}_\d+_?\w+?$", expand=True)

df_env["Scount"] = df_env["SequenceName"].str.extract("(^\d+-\d+)_\w{2,4}_\d+_?\w+?$", expand=True)

df_int["Scount"] = df_int["SequenceName"].str.extract("(^\d+-\d+)_\w{2,4}_\d+_?\w+?$", expand=True)


# Change the position of this column from last to first in all dfs
col1 = df_prrt.pop('Scount')
df_prrt.insert(0, 'Scount', col1)

col2 = df_env.pop('Scount')
df_env.insert(0, 'Scount', col2)

col3 = df_int.pop('Scount')
df_int.insert(0, 'Scount', col3)

# Change data type string -> float
df_prrt["Comet_PRRT_Comment"] = pd.to_numeric(df_prrt["Comet_PRRT_Comment"], downcast="float")

# Make a decision
for i, row in df_prrt.iterrows():
    if row["Stanford_PRRT_Subtype"] == row["Comet_PRRT_Subtype"] :
        df_prrt.at[i, ["PRRT_Subtype"]] = row["Stanford_PRRT_Subtype"]
    elif row["Comet_PRRT_Subtype"] == "_Seq. nicht klassifizierbar":
        df_prrt.at[i, ["PRRT_Subtype"]] = "_Seq. nicht klassifizierbar"
    else:
        df_prrt.at[i, ["PRRT_Subtype"]] = "Manual"


# Change data type string -> float
df_int["Comet_INT_Comment"] = pd.to_numeric(df_int["Comet_INT_Comment"], downcast="float")

# Make a decision
for i, row in df_env.iterrows():
    if row["Rega_ENV_Subtype"][0] == row["Comet_ENV_Subtype"] and len(row["Rega_ENV_Subtype"]) < 3 and row["Comet_ENV_Comment"] > 45:
        df_env.at[i, ["ENV_Subtype"]] = row["Comet_ENV_Subtype"]
    elif row["Comet_ENV_Subtype"] == "_Seq. nicht klassifizierbar":
        df_env.at[i, ["ENV_Subtype"]] = "_Seq. nicht klassifizierbar"
    else:
        df_env.at[i, ["ENV_Subtype"]] = "Manual"
    

# Change data type string -> float
df_env["Comet_ENV_Comment"] = pd.to_numeric(df_env["Comet_ENV_Comment"], downcast="float")

# Make a decision
for i, row in df_int.iterrows():
    if row["Stanford_INT_Subtype"] == row["Comet_INT_Subtype"] :
        df_int.at[i, ["INT_Subtype"]] = row["Stanford_INT_Subtype"]
    elif row["Comet_INT_Subtype"] == "_Seq. nicht klassifizierbar":
        df_int.at[i, ["INT_Subtype"]] = "_Seq. nicht klassifizierbar"
    else:
        df_int.at[i, ["INT_Subtype"]] = "Manual"

print(df_prrt[["SequenceName","Rega_PRRT_Subtype", "Stanford_PRRT_Subtype", "Comet_PRRT_Subtype", "PRRT_Subtype"]].head(50))

print(df_env[["SequenceName","Rega_ENV_Subtype", "Stanford_ENV_Subtype", "Comet_ENV_Subtype", "ENV_Subtype"]].head(50))

print(df_int[["SequenceName","Rega_INT_Subtype", "Stanford_INT_Subtype", "Comet_INT_Subtype", "INT_Subtype"]].head(50))

# Prepare a clean .csv file
df_prrt.to_csv("decision_MS95_PRRT_20M.csv", sep=",", index=False, encoding="utf-8")

# Prepare a clean .csv file
df_env.to_csv("decision_MS95_ENV_20M.csv", sep=",", index=False, encoding="utf-8")

# Prepare a clean .csv file
df_int.to_csv("decision_MS95_ENV_20M.csv", sep=",", index=False, encoding="utf-8")