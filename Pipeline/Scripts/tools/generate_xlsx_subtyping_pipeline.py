#!/usr/bin/env python3

# Import libraries
import sys
import argparse
import pandas as pd
from Bio import SeqIO


def create_excels(args):
    prrt_scounts = []
    int_scounts = []
    env_scounts = []
    prrt_headers = []
    int_headers = []
    env_headers = []
    prrt_sequences = []
    int_sequences = []
    env_sequences = []
    prrt_obj = SeqIO.parse(open(args.prrt),"fasta")
    int_obj = SeqIO.parse(open(args.int),"fasta")
    env_obj = SeqIO.parse(open(args.env),"fasta")
    
    for fasta in prrt_obj:
        prrt_scounts.append(fasta.id.split("_")[0])
        prrt_headers.append(fasta.id)
        prrt_sequences.append(str(fasta.seq))
    
    for fasta in int_obj:
        int_scounts.append(fasta.id.split("_")[0])
        int_headers.append(fasta.id)
        int_sequences.append(str(fasta.seq))
       
    for fasta in env_obj:
        env_scounts.append(fasta.id.split("_")[0])
        env_headers.append(fasta.id)
        env_sequences.append(str(fasta.seq))
    
    # Create dictionaries for each fragment
    prrt_dict = {"Scount": prrt_scounts, "Header": prrt_headers, "Sequenz": prrt_sequences}
    int_dict = {"Scount": int_scounts, "Header": int_headers, "Sequenz": int_sequences}
    env_dict = {"Scount": env_scounts, "Header": env_headers, "Sequenz": env_sequences}

    # Convert dictionaries to a pandas dataframe
    prrt_df = pd.DataFrame(prrt_dict)
    int_df = pd.DataFrame(int_dict)
    env_df = pd.DataFrame(env_dict)
        
    # Look up for PRRT's Scount, if it is not present in INT and ENV: add tag _nichtSequenziert and empty string for "Sequenz" column
    # _nichtSequenziert (Translation: _notSequenced) 
    for scount in prrt_scounts:
        if scount not in int_scounts:
            # Creating a new row
            new_row = {"Scount": scount, "Header": scount + "_INT_20" + "_nichtSequenziert", "Sequenz": ""}
            # Inserting the new row
            int_df.loc[len(int_df)] = new_row
            # Reset the index
            int_df = int_df.reset_index(drop=True)
        if scount not in env_scounts:
            # Creating a new row
            new_row = {"Scount": scount, "Header": scount + "_ENV_20" + "_nichtSequenziert", "Sequenz": ""}
            # Inserting the new row
            env_df.loc[len(env_df)] = new_row
            # Reset the index
            env_df = env_df.reset_index(drop=True)
    

    # Sort df by Scount
    prrt_df = prrt_df.sort_values(by=["Scount"])
    int_df = int_df.sort_values(by=["Scount"])
    env_df = env_df.sort_values(by=["Scount"])
    
    print(prrt_df.tail())
    print(int_df.tail())

    # Create excel files for each fragment          
    prrt_df.to_excel(args.prefix + "_Seqs_PRRT_CO20_V5.xlsx", index=False, encoding="utf-8")
    int_df.to_excel(args.prefix + "_Seqs_INT_CO20_V5.xlsx", index=False, encoding="utf-8")
    env_df.to_excel(args.prefix + "_Seqs_ENV_CO20_V5.xlsx", index=False, encoding="utf-8")

  


def main():
    parser=argparse.ArgumentParser(description = "Generate .xlsx for PRRT, INT, and ENV multyfastas")
    parser.add_argument("-p", "--prrt", help="PRRT fasta input file", dest = "prrt", type = str, required=True)
    parser.add_argument("-i", "--int", help="INT fasta input file", dest="int", type = str, required=True)
    parser.add_argument("-e", "--env", help="ENV fasta input file", dest = "env", type = str, required=True)
    parser.add_argument('-n', "--name", help="Prefix for a file name (e.g. 2024, Test)", dest="prefix", type=str, required=True)
    parser.add_argument("-v", "--verbose", help="verbose", dest="verbose", action='store_true')
    parser.set_defaults(func = create_excels)
    args=parser.parse_args()
    args.func(args)

if __name__=="__main__":
	main()
     
