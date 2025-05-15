#!/usr/bin/env python3

# Import libraries
import argparse
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import re


# Global variables 
_args = None

def initialise():
    '''
    Parse command-line arguments.
    '''
    global _args
    parser = argparse.ArgumentParser( description="A script to collect all intermediate reports in one final report" )
    parser.add_argument( "-p", "--prrt", required=True, help="Path to PRRT .xlsx file." )
    parser.add_argument( "-i", "--int", required=True, help="Path to INT .xlsx file." )
    _args = parser.parse_args()
    return


def extract_dataset_name(fpath):
    ''' Extract dataset name from PRRT excel file. '''
    dataset_name = fpath.rsplit("/")[-1].split("_")[1]
    print("Dataset name is {}".format(dataset_name))
    return dataset_name

def load_prrt(fpath):
    ''' Load and read excel PRRT file that contains subtyping assignments. '''
    df_full_prrt = pd.read_excel(fpath)
    prrt = df_full_prrt.loc[:,["Scount", "PRRT_Subsubtype"]]
    print("Loaded PRRT file, shape={}".format(prrt.shape))
    return prrt


def load_int(fpath):
    ''' Load and read excel INT file that contains subtyping assignments. '''
    df_full_int = pd.read_excel(fpath)
    int = df_full_int.loc[:,["Scount", "INT_Subsubtype"]]
    print("Loaded INT file, shape={}".format(int.shape))
    return int


def merge_dfs(prrt, int):
    try:
        # Merge tables
        merged_dfs = prrt.merge(int, on = "Scount", how = "outer")
        # Rename two first columns 
        merged_dfs.rename(columns = {"Scount":"Sample_ID", 
                                    "PRRT_Subsubtype": "Subtype_PRRT",
                                    "INT_Subsubtype": "Subtype_INT"}, inplace = True)
    
        # Strip white space
        merged_dfs = merged_dfs.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        # Initiate empty column
        merged_dfs["Subtype_ENV"] = "_notSequenced"

   
    except pd.errors.MergeError as e:
        print("Merge failed. Check shapes of you input tables: {}, {}, {}").format(prrt.shape, int.shape, env.shape)

    return merged_dfs

def hivtype_report(merged_dfs):
    report = merged_dfs.copy()
    
    # Initiate empty column
    report["Subtype"] = None

    # Initiate special cases
    special_cases = ["_notClassified",  "Manual", "_notSequenced"]

    # Make a decision
    for i, row in report.iterrows():
        if row["Subtype_PRRT"] == row["Subtype_INT"]:
            report.at[i, ["Subtype"]] = row["Subtype_PRRT"]
        elif row["Subtype_PRRT"] not in special_cases and row["Subtype_INT"] in special_cases:
            report.at[i, ["Subtype"]] = row["Subtype_PRRT"]

        elif row["Subtype_INT"] not in special_cases and row["Subtype_PRRT"] in special_cases:
            report.at[i, ["Subtype"]] = row["Subtype_INT"]     
    
        else:
            report.at[i, ["Subtype"]] = "Manual"
    
    # Sort df by Sample_ID column
    report.sort_values(by=["Sample_ID"], inplace=True)
    return report


def save_hivtype_outputs(report, dataset_name):
    ''' Write output. '''
    report.to_excel(dataset_name +"_report.xlsx", index=False, encoding="utf-8")
    print("HIVtype report is saved as {} with .xlxs extensions.".format(dataset_name))


def main():
    ''' Create a final report. '''
    dataset_name = extract_dataset_name(_args.prrt)
    prrt = load_prrt(_args.prrt)
    int = load_int(_args.int)
    merged_dfs = merge_dfs(prrt, int)
    report = hivtype_report(merged_dfs)
    save_hivtype_outputs(report, dataset_name)

if __name__ == '__main__':
    initialise()
    main()
