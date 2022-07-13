#!/bin/python

"""
This is a script to convert .json to .csv.
This code though does not provide a desired result (a clean .csv file).
"""

import json
import pandas as pd

with open('baker.json', encoding='utf-8') as inputfile:
    data = json.loads(inputfile.read())

df = pd.json_normalize(data)
print(df[['subtypeText', 'drugResistance']])
#print(df.columns)
df.to_csv('baker.csv', encoding='utf-8', index=False)
