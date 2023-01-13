# Import libraries
import pandas as pd
import sys


for infilename in sys.argv[1:]:
    name0 = infilename.rsplit("/")[-1] # gives a file name.csv
    list_of_substrings = name0.split("_")
    if "tag" in list_of_substrings and "PRRT" in list_of_substrings:
        df_tag_prrt = pd.read_csv(infilename, sep = ",")
        name1 = name0.split("tag_")[-1].split(".")[-2]
    if "tag" in list_of_substrings and "INT" in list_of_substrings:
        df_tag_int = pd.read_csv(infilename, sep = ",")
        name3 = name0.split("tag_")[-1].split(".")[-2]
    if "decision" in list_of_substrings and "PRRT" in list_of_substrings:
        df_prrt = pd.read_csv(infilename, sep = ",")
        name4 = name0.split("decision_")[-1].split(".")[-2]
    if "decision" in list_of_substrings and "INT" in list_of_substrings:
        df_int = pd.read_csv(infilename, sep = ",")
        name6 = name0.split("decision_")[-1].split(".")[-2]

outfilename = sys.argv[2]

# Join tables
df_full_prrt = pd.merge(df_tag_prrt, df_prrt, on = "SequenceName", how = "left")

df_full_int = pd.merge(df_tag_int, df_int, on = "SequenceName", how = "left")


df_full_prrt = df_full_prrt.sort_values(by=["SequenceName"])
df_full_prrt["PRRT_Subtype"] = df_full_prrt["PRRT_Subtype"].fillna(df_full_prrt["PRRT_Info"])


df_full_int = df_full_int.sort_values(by=["SequenceName"])
df_full_int["INT_Subtype"] = df_full_int["INT_Subtype"].fillna(df_full_int["INT_Info"])


# Add a columns with sequence length
df_full_prrt["SeqLength"] = df_full_prrt["Sequenz"].str.len()
df_full_int["SeqLength"] = df_full_int["Sequenz"].str.len()


# Change the position of SeqLength column from last to next to last in all dfs
col1 = df_full_prrt.pop("SeqLength")
df_full_prrt.insert(2, "SeqLength", col1)

col3 = df_full_int.pop("SeqLength")
df_full_int.insert(2, "SeqLength", col3)


# Create 'Scount' column in dfs
df_full_prrt["Scount"] = df_full_prrt["SequenceName"].str.extract("(^\d+-\d+)_\w{2,4}_\d+_?\w+?$", expand=True)

df_full_int["Scount"] = df_full_int["SequenceName"].str.extract("(^\d+-\d+)_\w{2,4}_\d+_?\w+?$", expand=True)



# Delete a control sample with no Scount
df_full_prrt = df_full_prrt.dropna(subset=["Scount"])
df_full_int = df_full_int.dropna(subset=["Scount"])


# Let "Scount" be the first column 
col4 = df_full_prrt.pop("Scount")
df_full_prrt.insert(0, "Scount", col4)


col6 = df_full_int.pop("Scount")
df_full_int.insert(0, "Scount", col6)

# Create "Repeat" coolumns
df_full_prrt["Repeat"] = df_full_prrt["SequenceName"].str.extract("^\d+-\d+_\w{2,4}_\d+(repeat\d{1})?$", expand=True)

df_full_int["Repeat"] = df_full_int["SequenceName"].str.extract("^\d+-\d+_\w{2,4}_\d+(repeat\d{1})?$", expand=True)



# Prepare a clean .xlsx file
df_full_prrt.to_excel("full_" + name4 + ".xlsx", index=False, encoding="utf-8")
df_full_int.to_excel("full_" + name6 + ".xlsx", index=False, encoding="utf-8")

