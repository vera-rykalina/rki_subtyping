import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_excel("MS95_subtype_uploads.xlsx")
#plt.style.use('ggplot')
sns.set_style("darkgrid")
fig, ax = plt.subplots(figsize=(10, 6))



count_plot = sns.countplot(y="Subtyp_Summe", data=df, 
                           palette="twilight",
                           order = df["Subtyp_Summe"].value_counts().index)
plt.savefig('subtype_counts.png') # Save that figure


ax.legend(title="HIV-1 Genotyping", fontsize=16, title_fontsize=20)
plt.xlabel("Count")
plt.ylabel("Total Subtype by PR, RT, INT, and ENV")
sns.despine(right = True)
plt.show()
plt.savefig('subtype_counts.png') # save that figure