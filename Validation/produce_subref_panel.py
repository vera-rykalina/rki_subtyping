'''
This script produces an organized subtype reference panel using LANL dowloaded fasta file and creates an accession list as txt file 
'''

# To procudece tsv from LANL multifasta use:
# seqkit seq -u subref_any_genome_filtered.fasta | seqkit fx2tab -l -Q -H -o subref_any_genome_filtered.tsv

import numpy as np
import pandas as pd
import sys
from textwrap import wrap
import openpyxl
import natsort as ns


# Open tsv file
infilename = sys.argv[1]

f = open(infilename, "rb")
df = pd.read_csv(f, sep='\t', header=0)
f.close()

# Rename column names
df = df.rename(columns={"#name": "Name", "seq": "Sequence", "length" : "Length"})

# Add columns
df["Subtype"] = df["Name"].str.split(".", n=1, expand=True)[0]
df["Country"] = df["Name"].str.split(".", expand=True)[1]
df["Year"] = df["Name"].str.split(".", expand=True)[2]
df["Accession"] = df["Name"].str.rsplit(".", n=1, expand=True)[1]



# Create a list of to date partial genomes (to be replaced with full genomes with time)
partial_genomes = [
"78_cpx.CN.2013.YNTC88.KU161145",
"78_cpx.CN.2013.YNTC35.KU161144",
"78_cpx.CN.2013.YNTC19.KU161143",
"82_cpx.MM.2013.mSSDU75.KU820845",
"82_cpx.MM.2013.mSSDU191.KU820836",
"82_cpx.MM.2013.mSSDU160.KU820831",
"82_cpx.MM.2013.mSSDU12.KU820825",
"83_cpx.MM.2013.mSSDU94.KU820847",
"83_cpx.MM.2013.mSSDU151.KU820829",
"83_cpx.MM.2013.mSSDU137.KU820826",
"83_cpx.MM.2013.mSSDU109.KU820823",
"86_BC.CN.2013.15YNHS26.KX582251",
"86_BC.CN.2013.15YNHS23.KX582250",
"86_BC.CN.2013.15YNHS18.KX582249",
"116_0108.CN.2016.16YN253.MT624749",
"116_0108.CN.2014.14YN263.MT624747",
"118_BC.CN.2017.YN287_168.MZ063029",
"118_BC.CN.2014.YN245F.MZ063028",
"118_BC.CN.2013.YN23II.MZ063027",
"124_cpx.AO.2009.ANG.78.ON962804",
"130_A1B.CY.2019.CY590.OP781328",
"131_A1B.CY.2020.CY710.OP781330",
"131_A1B.CY.2020.CY697.OP781329",
"138_cpx.CY.2021.CY842.OP894083",
"138_cpx.CY.2021.CY824.OP894082",
"138_cpx.CY.2021.CY805.OP894081",
"138_cpx.CY.2019.CY639.OP894080"
]

# Add a "Genome" column to mark completeness of genome
df["Genome"] = np.where(df["Name"].isin(partial_genomes), "partial", "complete")




# Sort by "Subtype" and "Length"
df = df.sort_values(by = ["Subtype", "Length"], ascending = [True, False])



# Set a number of sequences to be per subtype
N = 4
df = df.groupby("Subtype", as_index = False).nth[:N]


# Add a "InGroupCount" columns to show number of sequences per subtype
df["InGroupCount"] = df.groupby("Subtype")["Subtype"].transform("count")



# Create a non-CRF list
non_crf = ["A1","A2","A3","A4","A5","A6","A7","A8",
            "B", "C", "D",
            "F1", "F2",
            "G", "H", "J", "K", "L", "U"
            ]

# Add a "Genome" column to mark completeness of genome
df["Subtype"] = np.where(df["Subtype"].isin(non_crf), df["Subtype"], "CRF" + df["Subtype"])

# Add a "Type" column
df["Type"] = np.where(df["Subtype"].isin(non_crf), "Pure", "Recombinant")


# Sort by "Subtype" with natsort to order numbers correctly
df = df.sort_values(by = ["Type","Subtype"], key = ns.natsort_keygen(alg=ns.REAL))

# Recreate a header with -Ref- prefix
df["Header"] = "Ref." + df["Subtype"] + "." + df["Country"] + "." + df["Year"] + "." + df["Accession"]


# Convert a pandas dataframe to a .csv file
df.to_csv("fl_subref_panel.csv", index=False, sep=",", encoding="utf-8")


# Get fasta from csv file
headers = []
sequences = []
accessions = []

for i, row in df.iterrows():
        headers.append(row["Header"])
        sequences.append(row["Sequence"])
        accessions.append(row["Accession"])


# Write into a fasta file
with open("fl_subref_panel.fasta", "w") as file:
    for i in range(len(headers)):
        file.writelines(">" + headers[i])
        file.writelines("\n")
        file.writelines("\n".join(wrap(sequences[i], 60)))
        file.writelines("\n")


# Write into a txt file accession numbers
with open("fl_subref_panel_accession.txt", "w") as file:
    for i in range(len(accessions)):
         file.writelines(accessions[i])
         file.writelines("\n")
     
     