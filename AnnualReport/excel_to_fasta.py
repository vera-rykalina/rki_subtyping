import pandas as pd


#path = "HIVDB_request_Scounts2022_for_Jahresauswertung_PRRT.xlsx"
#df = pd.read_excel(path)

#print(df)
#print(df["Sequenz"].iloc[0])

#df['Header'] = df['Header'].map(lambda x: str(x)[1:-2])


#for i, row in df.iterrows():
#    print(">", row["Header"], '\n' , row["Sequenz"], sep='')

def ex_fasta(fastafile):
    s = ''
    df = pd.read_excel(fastafile)
    df['Header'] = df['Header'].map(lambda x: str(x)[1:-1])
    for i, row in df.iterrows():
        s += f">{row['Header']}\n{row['Sequenz']}\n"
    return s


with open("resistance.fasta", "w") as file:
    output = ex_fasta("HIVDB_request_Scounts2022_for_Jahresauswertung_PRRT.xlsx")
    file.writelines(output)
