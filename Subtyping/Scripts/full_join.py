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

# Add a columns with sequence length
df_full_prrt["SeqLength"] = df_full_prrt["Sequenz"].str.len()
df_full_int["SeqLength"] = df_full_int["Sequenz"].str.len()
df_full_env["SeqLength"] = df_full_env["Sequenz"].str.len()


# Change the position of SeqLength column from last to next to last in all dfs
col1 = df_full_prrt.pop("SeqLength")
df_full_prrt.insert(2, "SeqLength", col1)

col2 = df_full_env.pop("SeqLength")
df_full_env.insert(2, "SeqLength", col2)

col3 = df_full_int.pop("SeqLength")
df_full_int.insert(2, "SeqLength", col3)


# Remove non-relevant content
df_full_env["Stanford_ENV_Subtype"] = None
df_full_env["Stanford_ENV_Comment"] = None

# Prepare a clean .xlsx file
df_full_prrt.to_excel("full_" + name4 + ".xlsx", index=False, encoding="utf-8")
df_full_env.to_excel("full_" + name5 + ".xlsx", index=False, encoding="utf-8")
df_full_int.to_excel("full_" + name6 + ".xlsx", index=False, encoding="utf-8")

