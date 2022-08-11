#!/bin/python3

# Import libraries
import pandas as pd
import sys
import re


# Read .csv file
df_prrt = pd.read_csv("with_decision_PRRT_joint.csv", sep = ",")
df_env = pd.read_csv("with_decision_ENV_joint.csv", sep = ",")
df_int = pd.read_csv("with_decision_INT_joint.csv", sep = ",")
df_tag_prrt = pd.read_csv("tagged_MS95_Seqs_PRRT_CO20_V5.csv", sep = ",")
df_tag_env = pd.read_csv("tagged_MS95_Seqs_ENV_CO20_V5.csv", sep = ",")
df_tag_int = pd.read_csv("tagged_MS95_Seqs_INT_CO20_V5.csv", sep = ",")


# Join tables
df_full_prrt = pd.merge(df_tag_prrt, df_prrt, on = "Scount", how = "outer")

df_full_env = pd.merge(df_tag_env, df_env, on = "Scount", how = "outer")

df_full_int = pd.merge(df_tag_int, df_int, on = "Scount", how = "outer")

# Select only what is needed
#df_final = df_final.loc[:,["Scount", "PRRT_Subtype","INT_Subtype", "ENV_Subtype"]]

#df_final["PRRT_Subtype"] = df_final["PRRT_Subtype"].fillna(df_prrt["PRRT_Subtype_Decision"])


# Prepare a clean .csv file
df_full_prrt.to_csv("full_prrt.csv", sep=",", index=False, encoding="utf-8")
df_full_env.to_csv("full_env.csv", sep=",", index=False, encoding="utf-8")
df_full_int.to_csv("full_int.csv", sep=",", index=False, encoding="utf-8")
