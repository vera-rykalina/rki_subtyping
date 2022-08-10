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
df_final = pd.concat([df_tag_prrt, df_tag_env, df_tag_int], axis=1)


# Select only what is needed
df_final = df_final.loc[:,["Scount", "PRRT_Subtype","INT_Subtype", "ENV_Subtype"]]

df_final["PRRT_Subtype"] = df_final["PRRT_Subtype"].fillna(df_prrt["PRRT_Subtype_Decision"])
df_final["INT_Subtype"] = df_final["INT_Subtype"].fillna(df_int["INT_Subtype_Decision"])
df_final["ENV_Subtype"] = df_final["ENV_Subtype"].fillna(df_env["ENV_Subtype_Decision"])

print(df_final)

# Prepare a clean .csv file
df_final.to_csv("final_report.csv", sep=",", index=False, encoding="utf-8")
