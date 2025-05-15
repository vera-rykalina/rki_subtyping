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
    parser = argparse.ArgumentParser( description="A script to generate a plot from final report file" )
    parser.add_argument( "-r", "--report", required=True, help="Report .xlsx file." )
    _args = parser.parse_args()
    return

def extract_dataset_name(fpath):
    ''' Extract dataset name from report excel file. '''
    dataset_name = fpath.rsplit("/")[-1].split("_")[0]
    print("Dataset name is {}".format(dataset_name))
    return dataset_name


def load_report(fpath):
    ''' Load and read excel report file that contains final subtyping assignments. '''
    report = pd.read_excel(fpath)
    print("Loaded report file, shape={}".format(report.shape))
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
    plt.tight_layout()
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



def save_hivtype_outputs(countplot_fig, dataset_name):
    ''' Write output. '''
    countplot_fig.savefig(dataset_name + "_countplot.png", dpi = 300, bbox_inches="tight")
    print("HIVtype plot is saved as {} with .png extensions.".format(dataset_name))


def main():
    ''' Generate a final plot. '''
    dataset_name = extract_dataset_name(_args.report)
    report = load_report(_args.report)
    countplot_fig = plot(report, dataset_name)
    save_hivtype_outputs(countplot_fig, dataset_name)

if __name__ == '__main__':
    initialise()
    main()
