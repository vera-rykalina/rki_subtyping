#!/usr/bin/env python3

# Import libraries
import pandas as pd
import sys


infilename = sys.argv[1]
outfilename = sys.argv[2]


for infilename in sys.argv[1:]:
    name1 = infilename.rsplit("/")[-1] # gives a file name.csv
    name2 = name1.split("_")[-2] # gives a middle part after splitting by "_"
    name3 = name1.split("joint_")[-1].split(".")[-2] # cuts .csv
    list_of_substrings = name1.split("_")
    df = pd.read_csv(infilename, sep = ",")
    
    # Change data type string -> float
    df["Comet_" + name2 + "_Comment"] = pd.to_numeric(df["Comet_" + name2 + "_Comment"], downcast="float")

    # Create a list of rare subtypes and groups (L, O, N, P)
    rare_subtypes_groups = ["L", "O", "N", "P"]
    
    # Create a list of known subsubtypes (for A and F)
    subsubtypes = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "F1", "F2"]
   
    if "PRRT" in list_of_substrings or "INT" in list_of_substrings:
        for i, row in df.iterrows():
            if row["Geno2Pheno_" + name2 + "_Subtype"] == row["Comet_" + name2 + "_Subtype"] and row["Comet_" + name2 + "_Comment"] >= 50 and row["Comet_" + name2 + "_Subtype"] in rare_subtypes_groups:
                df.at[i, [name2 + "_Subtype"]] = row["Comet_" + name2 + "_Subtype"]

            elif row["Stanford_" + name2 + "_Subtype"] == row["Comet_" + name2 + "_Subtype"] and row["Comet_" + name2 + "_Comment"] >= 50 and row["Comet_" + name2 + "_Subtype"] not in subsubtypes:
                df.at[i, [name2 + "_Subtype"]] = row["Stanford_" + name2 + "_Subtype"]

            elif row["Stanford_" + name2 + "_Subtype"] == row["Comet_" + name2 + "_Subtype"].split(")")[0].split(" ")[-1] and row["Comet_" + name2 + "_Comment"] == 0 and row["Comet_" + name2 + "_Subtype"] not in subsubtypes and row["Comet_" + name2 + "_Subtype"] != "Unassigned":
                df.at[i, [name2 + "_Subtype"]] = row["Stanford_" + name2 + "_Subtype"]

            elif row["Stanford_" + name2 + "_Subtype"][0] == row["Comet_" + name2 + "_Subtype"][0] and row["Comet_" + name2 + "_Comment"] >= 50 and row["Comet_" + name2 + "_Subtype"] in subsubtypes:
                df.at[i, [name2 + "_Subtype"]] = row["Comet_" + name2 + "_Subtype"][0]

            else:
                df.at[i, [name2 + "_Subtype"]] = "Manual" 
        
        # Subsubtyping
        
        for i, row in df.iterrows():
            if row["Geno2Pheno_" + name2 + "_Subtype"] == row["Comet_" + name2 + "_Subtype"] and row["Comet_" + name2 + "_Comment"] >= 50 and row["Comet_" + name2 + "_Subtype"] in subsubtypes:
                df.at[i, [name2 + "_Subsubtype"]] = row["Comet_" + name2 + "_Subtype"]
            
            elif row["Geno2Pheno_" + name2 + "_Subtype"] != row["Comet_" + name2 + "_Subtype"] and row["Comet_" + name2 + "_Comment"] >= 50 and row["Comet_" + name2 + "_Subtype"] in subsubtypes:
                df.at[i, [name2 + "_Subsubtype"]] = "Manual"
            
            else: 
                df.at[i, [name2 + "_Subsubtype"]] = row[name2 + "_Subtype"]
        

        # Prepare .csv file
        df.to_csv("decision_" + name3 + ".csv", sep=",", index=False, encoding="utf-8") 

    if "ENV" in list_of_substrings:
        for i, row in df.iterrows():
            if row["Geno2Pheno_" + name2 + "_Subtype"] == row["Comet_" + name2 + "_Subtype"] and row["Comet_" + name2 + "_Comment"] >= 50 and row["Comet_" + name2 + "_Subtype"] in rare_subtypes_groups:
                df.at[i, [name2 + "_Subtype"]] = row["Comet_" + name2 + "_Subtype"]

            elif row["Geno2Pheno_" + name2 + "_Subtype"] == row["Comet_" + name2 + "_Subtype"] and row["Comet_" + name2 + "_Comment"] >= 50 and row["Comet_" + name2 + "_Subtype"] in subsubtypes:
                df.at[i, [name2 + "_Subtype"]] = row["Comet_" + name2 + "_Subtype"][0]

            elif row["Geno2Pheno_" + name2 + "_Subtype"] == row["Comet_" + name2 + "_Subtype"] and row["Comet_" + name2 + "_Comment"] >= 50 and row["Comet_" + name2 + "_Subtype"] not in subsubtypes:
                df.at[i, [name2 + "_Subtype"]] = row["Comet_" + name2 + "_Subtype"]

            elif row["Geno2Pheno_" + name2 + "_Subtype"] != row["Comet_" + name2 + "_Subtype"] and row["Comet_" + name2 + "_Comment"] >= 70 and row["Comet_" + name2 + "_Subtype"] in subsubtypes:
                df.at[i, [name2 + "_Subtype"]] = row["Comet_" + name2 + "_Subtype"][0]
            
            elif row["Geno2Pheno_" + name2 + "_Subtype"] != row["Comet_" + name2 + "_Subtype"] and row["Comet_" + name2 + "_Comment"] >= 70 and row["Comet_" + name2 + "_Subtype"] not in subsubtypes:
                df.at[i, [name2 + "_Subtype"]] = row["Comet_" + name2 + "_Subtype"]
            
            else:
                df.at[i, [name2 + "_Subtype"]] = "Manual"
    
        # Subsubtyping
        
        for i, row in df.iterrows():
            if row["Geno2Pheno_" + name2 + "_Subtype"] == row["Comet_" + name2 + "_Subtype"] and row["Comet_" + name2 + "_Comment"] >= 50 and row["Comet_" + name2 + "_Subtype"] in subsubtypes:
                df.at[i, [name2 + "_Subsubtype"]] = row["Comet_" + name2 + "_Subtype"]
            
            elif row["Geno2Pheno_" + name2 + "_Subtype"] != row["Comet_" + name2 + "_Subtype"] and row["Comet_" + name2 + "_Comment"] >= 50 and row["Comet_" + name2 + "_Subtype"] in subsubtypes:
                df.at[i, [name2 + "_Subsubtype"]] = "Manual"
                       
            else: 
                df.at[i, [name2 + "_Subsubtype"]] = row[name2 + "_Subtype"]
        
        df.to_csv("decision_" + name3 + ".csv", sep=",", index=False, encoding="utf-8")
