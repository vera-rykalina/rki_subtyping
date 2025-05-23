#!/usr/bin/env python3

# Import libraries
import sys
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl


# Open .xlsx file
infilename = sys.argv[1]
outfilename = sys.argv[2]

# Read .xlsx file
f = open(infilename, "rb")
df=pd.read_excel(f)
f.close()

name1 = infilename.rsplit("/")[-1]
name2 = name1.split("_")[0]
name3 = name1.split(".")[-2]

if "Subtype" not in df.columns:
    df.rename(columns = {"Subtyp_Summe":"Subtype"}, inplace = True)

# Strip white space
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

#sns.set_style("whitegrid")
#sns.set_context("poster")
#fig, ax = plt.subplots(figsize=(22, 12))
sns.set_style("darkgrid")
fig, ax = plt.subplots(figsize=(16, 8))




count_plot = sns.countplot(y="Subtype", data=df, 
                           #palette="twilight",
                           palette = "GnBu_d",
                           #palette = "Blues_d",
                           #palette="viridis",
                           order = df["Subtype"].value_counts().index)


# Create a legend with RUN_NUMBER (e.g. MS95)
ax.legend(title=name2, fontsize=12, title_fontsize=20, loc="lower right")


#ax.legend(title=name2, fontsize=24, title_fontsize=30, loc="lower right")
#plt.xlabel("Count", fontsize=32)
#plt.ylabel("Subtype", fontsize=32)
#plt.title("HIV-1 Subtyping (Stanford, Comet, Rega, Geno2Pheno)", fontsize=36)
#plt.tick_params(axis="both", which="major", labelsize=24)

#for container in ax.containers:
#    ax.bar_label(container, fontsize = 26) 

# Add lebels
ax.set(xlabel="Count", ylabel="Subtype", title = "HIV-1 Subtyping (Stanford, Comet, Rega, Geno2Pheno)")

# Add values to bars
for container in ax.containers:
    ax.bar_label(container) 

# Save figure
plt.savefig(name2 + "_subtype_counts.png", dpi = 300, bbox_inches="tight") 
# plt.show()