import sys
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns


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

sns.set_style("darkgrid")
sns.set_context("talk")
fig, ax = plt.subplots(figsize=(16, 8))



count_plot = sns.countplot(y="Subtyp_Summe", data=df, 
                           #palette="twilight",
                           palette = "GnBu_d",
                           #palette="viridis",
                           order = df["Subtyp_Summe"].value_counts().index)


# Create a legend with RUN_NUMBER (e.g. MS95)
ax.legend(title=name2, fontsize=16, title_fontsize=20)

# Add lebels
ax.set(xlabel="Count", ylabel="Subtype Sum", title = "HIV-1 Subtyping (Stanford, Comet, Rega)")

# Add values to bars
for container in ax.containers:
    ax.bar_label(container) 

# Save figure
plt.savefig(name2 + "_subtype_counts.png", dpi = 300) 
plt.show()