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
    parser.add_argument( "-e", "--env", required=True, help="Path to ENV .xlsx file." )
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


def load_env(fpath):
    ''' Load and read excel ENV file that contains subtyping assignments. '''
    df_full_env = pd.read_excel(fpath)
    env = df_full_env.loc[:,["Scount", "ENV_Subsubtype"]]
    print("Loaded ENV file, shape={}".format(env.shape))
    return env

def merge_dfs(prrt, int, env):
    try:
        # Merge tables
        merged_dfs = prrt.merge(int, on = "Scount", how = "outer").merge(env, on = "Scount", how = "outer")  
        # Rename two first columns 
        merged_dfs.rename(columns = {"Scount":"Sample_ID", 
                                    "PRRT_Subsubtype": "Subtype_PRRT",
                                    "INT_Subsubtype": "Subtype_INT", 
                                    "ENV_Subsubtype": "Subtype_ENV"}, inplace = True)
    
        # Strip white space
        merged_dfs = merged_dfs.applymap(lambda x: x.strip() if isinstance(x, str) else x)
   
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
        if row["Subtype_PRRT"] == row["Subtype_INT"] and row["Subtype_PRRT"] == row["Subtype_ENV"] and row["Subtype_PRRT"] not in special_cases:
            report.at[i, ["Subtype"]] = row["Subtype_PRRT"]
        
        elif row["Subtype_PRRT"] == row["Subtype_INT"] and row["Subtype_PRRT"] == row["Subtype_ENV"] and row["Subtype_PRRT"] == "_notSequenced":
            report.at[i, ["Subtype"]] = "_notSequenced"
    
        elif row["Subtype_PRRT"] == row["Subtype_INT"] and row["Subtype_ENV"] == "_notClassified" and row["Subtype_PRRT"] == "_notSequenced":
            report.at[i, ["Subtype"]] = "_notClassified"
    
        elif row["Subtype_ENV"] == row["Subtype_INT"] and row["Subtype_PRRT"] == "_notClassified" and row["Subtype_ENV"] == "_notSequenced":
            report.at[i, ["Subtype"]] = "_notClassified"
    
        elif row["Subtype_PRRT"] == row["Subtype_ENV"] and row["Subtype_INT"] == "_notClassified" and row["Subtype_PRRT"] == "_notSequenced":
            report.at[i, ["Subtype"]] = "_notClassified"
    
        elif row["Subtype_PRRT"] == row["Subtype_INT"] and row["Subtype_PRRT"] == row["Subtype_ENV"] and row["Subtype_PRRT"] in special_cases:
           report.at[i, ["Subtype"]] = "Manual"
    
        elif row["Subtype_PRRT"] == row["Subtype_INT"] and len(row["Subtype_PRRT"]) <=2 and len(row["Subtype_ENV"]) > 2 and row["Subtype_ENV"] not in special_cases:
           report.at[i, ["Subtype"]] = row["Subtype_ENV"]
    
        elif row["Subtype_PRRT"] == row["Subtype_ENV"] and len(row["Subtype_PRRT"]) <=2 and len(row["Subtype_INT"]) > 2 and row["Subtype_INT"] not in special_cases:
           report.at[i, ["Subtype"]] = row["Subtype_INT"]
    
        elif row["Subtype_INT"] == row["Subtype_ENV"] and len(row["Subtype_INT"]) <=2 and len(row["Subtype_PRRT"]) > 2 and row["Subtype_PRRT"] not in special_cases:
           report.at[i, ["Subtype"]] = row["Subtype_PRRT"]
    
        elif row["Subtype_PRRT"] == row["Subtype_INT"] and row["Subtype_ENV"] in special_cases:
           report.at[i, ["Subtype"]] = row["Subtype_PRRT"]
    
        elif row["Subtype_INT"] == row["Subtype_ENV"] and row["Subtype_PRRT"] in special_cases:
           report.at[i, ["Subtype"]] = row["Subtype_INT"]
    
        elif row["Subtype_PRRT"] == row["Subtype_ENV"] and row["Subtype_INT"] in special_cases:
           report.at[i, ["Subtype"]] = row["Subtype_PRRT"]

        elif row["Subtype_INT"] in special_cases and row["Subtype_ENV"] in special_cases and row["Subtype_PRRT"] not in special_cases:
           report.at[i, ["Subtype"]] = row["Subtype_PRRT"]
    
        elif row["Subtype_PRRT"] in special_cases and row["Subtype_ENV"] in special_cases and row["Subtype_INT"] not in special_cases:
           report.at[i, ["Subtype"]] = row["Subtype_INT"]
    
        elif row["Subtype_PRRT"] in special_cases and row["Subtype_INT"] in special_cases and row["Subtype_ENV"] not in special_cases:
           report.at[i, ["Subtype"]] = row["Subtype_ENV"]
    
        else:
           report.at[i, ["Subtype"]] = "Manual"
    
    # Sort df by Sample_ID column
    report.sort_values(by=["Sample_ID"], inplace=True)
    return report

def plot(report, dataset_name):
    if "Subtype" not in report.columns:
        report.rename(columns = {"Subtyp_Summe":"Subtype"}, inplace = True)
    # Strip white space
    report = report.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    
    # Graph
    #sns.set_context("poster")
    #sns.set_style("whitegrid")
    sns.set_style("darkgrid")
    fig, ax = plt.subplots(figsize=(18, 8))
    countplot = sns.countplot(y="Subtype", data=report, 
                              #palette = "Blues_d",
                              palette = "GnBu_d",
                              order = report["Subtype"].value_counts().index)


    # Create a legend with RUN_NUMBER (e.g. MS95)
    ax.legend(title=dataset_name, fontsize=12, title_fontsize=20, loc="lower right")
    
    # Add lebels
    ax.set(xlabel="Count", ylabel="Subtype", 
           title = "HIV-1 Subtyping (Stanford, Comet, Rega, Geno2Pheno)")

    # Add values to bars
    for container in ax.containers:
        ax.bar_label(container) 
    
    # Ticks
    plt.tick_params(axis="both", which="major", labelsize=6)
    
    # Save a figure
    countplot_fig = countplot.get_figure()
    return countplot_fig



def save_hivtype_outputs(report, countplot_fig, dataset_name):
    ''' Write output. '''
    report.to_excel(dataset_name +"_report.xlsx", index=False, encoding="utf-8")
    countplot_fig.savefig(dataset_name + "_countplot.png", dpi = 300, bbox_inches="tight")
    print("HIVtype report is saved as {} with .xlxs or .png extensions.".format(dataset_name))


def main():
    ''' Create a final report. '''
    dataset_name = extract_dataset_name(_args.prrt)
    prrt = load_prrt(_args.prrt)
    int = load_int(_args.int)
    env = load_env(_args.env)
    merged_dfs = merge_dfs(prrt, int, env)
    report = hivtype_report(merged_dfs)
    countplot_fig = plot(report, dataset_name)
    save_hivtype_outputs(report, countplot_fig, dataset_name)

if __name__ == '__main__':
    initialise()
    main()
