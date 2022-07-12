#!/bin/python3

import json
import pandas as pd



with open("baker.json") as f:
    data = json.load(f)

columns = {}
col_header = []
col_subtype = []
for index, sequence in enumerate(data):
    #print(sequence['subtypeText'])
    #print(index, sequence['subtypeText'])
    col_header.append(sequence["inputSequence"]["header"])
    col_subtype.append(sequence["subtypeText"])
    

columns["SequenceName"] = col_header
columns["Subtype%"] = col_subtype
df = pd.DataFrame(columns)


print(len(data))
print(type(data))
print(type(data[0]))
#print(df.head())

df[["Subtype", "Percent"]] = df["Subtype%"].str.split(" ", n=1, expand=True)
print(df.head())
print(df.tail())