import pandas as pd
import sys
from textwrap import wrap
import openpyxl

# Open tsv file
infilename = sys.argv[1]

f = open(infilename, "rb")
df1 = pd.read_csv(f, sep='\t', header=0)
f.close()

# Rename column names
df1 = df1.rename(columns={"#name": "Name", "seq": "Sequence", "length" : "Length"})

# Add columns
df1["Comment"] = df1["Name"].str.split(".", n=1, expand=True)[0]

# Create a comment to indicate origin of a sequence
df1.loc[df1["Comment"] != "Ref", "Comment"] = "LANL"
df1.loc[df1["Comment"] == "Ref", "Comment"] = "REF"

# Remove Ref in Name
df1["Name"] = df1["Name"].map(lambda x: x.lstrip("Ref."))


df1["Subtype"] = df1["Name"].str.split(".", n=1, expand=True)[0]
df1["Country"] = df1["Name"].str.split(".", expand=True)[1]
df1["Year"] = df1["Name"].str.split(".", expand=True)[2]

df1["Accession"] = df1["Name"].str.rsplit(".", n=1, expand=True)[1]


# Add a column Date
def change_year (year_string):
    if len(year_string) < 3 and year_string[0] != "x" and year_string[0] != "-" and int(year_string[0]) > 6 :
        year_string = "19" + year_string
    elif len(year_string) < 3 and year_string[0] != "x" and year_string[0] != "-" and int(year_string[0]) < 6:
        year_string = "20" + year_string
    elif len(year_string) < 3 and year_string[0] == "x":
        year_string = "-"
    return year_string
    
# df1["Date"] = [change_year(x) for x in df1["Year"]]

# Create Scount column
df1["Scount"] = range(1000, 1000 + df1.shape[0])
df1["Scount"] = "24-0" + df1["Scount"].astype(str)

# Convert a pandas dataframe to a .csv file
#df1.to_csv("env_validation_dataset.csv", index=False, sep=",", encoding="utf-8")
df1.to_csv("fl_validation_dataset.csv", index=False, sep=",", encoding="utf-8")

#########################################################################
f = open("fl_validation_dataset.csv", "rb")
df2 = pd.read_csv(f, sep=',', header=0)
f.close()


# Create columns
df2["Cutoff"] = "20"
#df2["Fragment"] = "_PRRT_"
#df2["Fragment"] = "_INT_"
#df2["Fragment"] = "_ENV_"
df2["Fragment"] = "_FL_"
df2["Header"] = df2["Scount"] + df2["Fragment"] + df2["Cutoff"]

# Rename "Sequence" to "Sequenz"
df2 = df2.rename(columns={"Sequence": "Sequenz"})


# Select only what is needed
df2 = df2.loc[:,["Scount", "Header", "Sequenz"]]
print(df2)

# Create output file
#df2.to_excel("VALIDATION_Seqs_PRRT_CO20_V5.xlsx", index=False)
#df2.to_excel("VALIDATION_Seqs_INT_CO20_V5.xlsx", index=False)
#df2.to_excel("VALIDATION_Seqs_ENV_CO20_V5.xlsx", index=False)


# Get fasta from csv file
names = []
sequences = []

for i, row in df2.iterrows():
        names.append(row["Header"])
        sequences.append(row["Sequenz"])

# Write into a fasta file (modify fragment name)
with open("VALIDATION_FL_20.fasta", "w") as file:
    for i in range(len(names)):
        file.writelines(">" + names[i])
        file.writelines("\n")
        file.writelines("\n".join(wrap(sequences[i], 60)))
        file.writelines("\n")


