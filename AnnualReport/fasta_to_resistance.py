#!/bin/python3

import json
import pandas as pd



with open("baker.json") as f:
    data = json.load(f)

columns = {}
col_header = []
col_strain = []
col_gene = []
col_class = []

for sequence in data:
    col_header.append(sequence["inputSequence"]["header"])
    col_strain.append(sequence["strain"]["name"])
    col_gene.append(sequence["drugResistance"][-2]["gene"]["name"])
    #col_class.append(sequence['drugResistance'][-2]['drugScores'][0]['drugClass']['name'])


col_drugClass = []
for cl in data[0]["drugResistance"][2]["drugScores"]:
    col_drugClass.append(cl["drugClass"]["name"])
print(col_drugClass)

columns["SequenceName"] = col_header
columns["Strain"] = col_strain
columns["Genes"] = col_gene
#columns["DrugClass"] = col_class
df = pd.DataFrame(columns)


print(len(data[0]["drugResistance"]))
print(type(data[0]["drugResistance"][2]['drugScores'][0]['drugClass']['name']))
print(data[0]["drugResistance"][2]['drugScores'][0]['drugClass']['name'])
print(type(data))
print(type(data[0]))



print(df.head())
print(df.tail())