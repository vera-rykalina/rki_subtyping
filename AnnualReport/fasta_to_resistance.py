#!/bin/python3

import json
from matplotlib.cbook import ls_mapper
import pandas as pd



with open("baker.json") as f:
    data = json.load(f)

columns = {}
col_header = []
col_strain = []
col_gene = []
col_class = []
col_ATV_score = []
col_ATV_level = []
col_ATV_interpretation = []

for index, sequence in enumerate(data):
   col_header.append(sequence["inputSequence"]["header"])
   col_strain.append(sequence["strain"]["name"])
   if index == 57 and sequence["drugResistance"][1]["drugScores"][0] != "PI":
    col_gene.append(sequence["drugResistance"][1]["gene"]["name"])
    col_class.append("NA")
    col_ATV_score.append("NA")
    col_ATV_level.append("NA")
    col_ATV_interpretation.append("NA")
    
   #if len(sequence["drugResistance"]) == 4:
   else:
    col_gene.append(sequence["drugResistance"][2]["gene"]["name"])
    col_class.append(sequence["drugResistance"][2]["drugScores"][0]["drugClass"]["name"])
    col_ATV_score.append(sequence["drugResistance"][2]["drugScores"][0]["score"])
    col_ATV_level.append(sequence["drugResistance"][2]["drugScores"][0]["level"])
    col_ATV_interpretation.append(sequence["drugResistance"][2]["drugScores"][0]["text"])
#    else:
#     print(index)
#     col_gene.append("NA")
#     col_class.append("NA")
#     col_ATV_score.append("NA")
#     col_ATV_level.append("NA")
#     col_ATV_interpretation.append("NA")

  
columns["SequenceName"] = col_header
columns["Strain"] = col_strain
columns["Genes"] = col_gene
columns["DrugClass"] = col_class
columns["ATV/r Score"] = col_ATV_score
columns["ATV/r Level"] = col_ATV_level
columns["ATV/r Interpretation"] = col_ATV_interpretation
df = pd.DataFrame(columns)

df.to_csv("resistance.csv", index=False, sep=",", encoding='utf-8')


print(df.head())
print(df.tail())