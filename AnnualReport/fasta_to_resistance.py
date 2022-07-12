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
    #NB!: Works with [-2] but won't with [2]!
    col_gene.append(sequence["drugResistance"][-2]["gene"]["name"])
    #NB!: The line below won't work at all!
    #col_class.append(sequence['drugResistance'][-2]['drugScores'][0]['drugClass']['name'])

# A loop to check the list content 
for cl in data[0]["drugResistance"][2]["drugScores"]:
    print(cl["drugClass"]["name"])


columns["SequenceName"] = col_header
columns["Strain"] = col_strain
columns["Genes"] = col_gene
#columns["DrugClass"] = col_class
df = pd.DataFrame(columns)


# Some quick check points
print(len(data[0]["drugResistance"]))
print(type(data[0]["drugResistance"][2]['drugScores'][0]['drugClass']['name']))
print(data[0]["drugResistance"][2]['drugScores'][0]['drugClass']['name'])
print(type(data))
print(type(data[0]))



print(df.head())
print(df.tail())