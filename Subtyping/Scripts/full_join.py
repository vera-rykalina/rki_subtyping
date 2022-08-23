#!/bin/python3

# Import libraries
import pandas as pd
import sys


for infilename in sys.argv[1:]:
    name0 = infilename.rsplit("/")[-1] # gives a file name.csv
    list_of_substrings = name0.split("_")
    if "tag" in list_of_substrings and "PRRT" in list_of_substrings:
        df_tag_prrt = pd.read_csv(infilename, sep = ",")
        name1 = name0.split("tag_")[-1].split(".")[-2]
    if "tag" in list_of_substrings and  "ENV" in list_of_substrings:
        df_tag_env = pd.read_csv(infilename, sep = ",")
        name2 = name0.split("tag_")[-1].split(".")[-2]
    if "tag" in list_of_substrings and "INT" in list_of_substrings:
        df_tag_int = pd.read_csv(infilename, sep = ",")
        name3 = name0.split("tag_")[-1].split(".")[-2]
    if "decision" in list_of_substrings and "PRRT" in list_of_substrings:
        df_prrt = pd.read_csv(infilename, sep = ",")
        name4 = name0.split("decision_")[-1].split(".")[-2]
    if "decision" in list_of_substrings and "ENV" in list_of_substrings:
        df_env = pd.read_csv(infilename, sep = ",")
        name5 = name0.split("decision_")[-1].split(".")[-2]
    if "decision" in list_of_substrings and "INT" in list_of_substrings:
        df_int = pd.read_csv(infilename, sep = ",")
        name6 = name0.split("decision_")[-1].split(".")[-2]

outfilename = sys.argv[2]

# Join tables
df_full_prrt = pd.merge(df_tag_prrt, df_prrt, on = "Scount", how = "left")

df_full_env = pd.merge(df_tag_env, df_env, on = "Scount", how = "left")

df_full_int = pd.merge(df_tag_int, df_int, on = "Scount", how = "left")



df_full_prrt["PRRT_Subtype"] = df_full_prrt["PRRT_Subtype"].fillna(df_full_prrt["PRRT_Info"])
df_full_prrt = df_full_prrt.sort_values(by=["Scount", "PRRT_Subtype"])

df_full_env["ENV_Subtype"] = df_full_env["ENV_Subtype"].fillna(df_full_env["ENV_Info"])
df_full_env = df_full_env.sort_values(by=["Scount", "ENV_Subtype"])

df_full_int["INT_Subtype"] = df_full_int["INT_Subtype"].fillna(df_full_int["INT_Info"])
df_full_int = df_full_int.sort_values(by=["Scount", "INT_Subtype"])


# Prepare a clean .xlsx file
df_full_prrt.to_excel("full_" + name4 + ".xlsx", index=False, encoding="utf-8")
df_full_env.to_excel("full_" + name5 + ".xlsx", index=False, encoding="utf-8")
df_full_int.to_excel("full_" + name6 + ".xlsx", index=False, encoding="utf-8")

