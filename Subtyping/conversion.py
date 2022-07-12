#!/bin/python

"""
import pandas as pd
# As of Pandas 1.01, json_normalize as pandas.io.json.json_normalize is deprecated and is now exposed in the top-level namespace.
# from pandas.io.json import json_normalize
from pathlib import Path
import json

# set path to file
p = Path(r'c:\some_path_to_file\test.json')

# read json
with p.open('r', encoding='utf-8') as f:
    data = json.loads(f.read())

# create dataframe
df = pd.json_normalize(data)
"""

import json
import pandas as pd

with open('baker.json', encoding='utf-8') as inputfile:
    data = json.loads(inputfile.read())

df = pd.json_normalize(data)
print(df[['subtypeText', 'drugResistance']])
#print(df.columns)
df.to_csv('baker.csv', encoding='utf-8', index=False)
