# HiVtype: A Semi-Automated Workflow for HIV-1 Subtyping

The aim of a pipeline is to automate a routine HIV-1 subtyping analysis, using Stanford (SierraPy), Comet (Rest API), Rega (manually generated .csv files via click or drop) and Geno2Pheno (manually generated .csv files via click or drop) tools. The pipeline is built with Nextflow and custom Python scripts. 

## Pipeline workflow
![Plot](Documentation/images/subtyping_pipeline.png)

Inputs of the pipeline include:

- .fasta files (fused PRRT, INT, ENV or fused PRRT and INT )
- .csv files (manually generated, using Rega online tool)
- .csv files (manually generated, using Geno2Pheno online tool)
- .fasta files of reference panels (subtype_origin_year_accession)
- (optional) .xlsx files (HIVpipe, contain information for invalid sequences)

  
```sh
├── AllSeqsCO20
│   ├── MS95_Seqs_ENV_CO20_V5.xlsx
│   ├── MS95_Seqs_INT_CO20_V5.xlsx
│   └── MS95_Seqs_PRRT_CO20_V5.xlsx
├── InputFasta
│   ├── MS95_ENV_20.fasta
│   ├── MS95_INT_20.fasta
│   └── MS95_PRRT_20.fasta
├── ManualRega
│   ├── Manual_Rega_MS95_ENV_20M.csv
│   ├── Manual_Rega_MS95_INT_20M.csv
│   └── Manual_Rega_MS95_PRRT_20M.csv
├── ManualRega
│   ├── Manual_Geno2Pheno_MS95_ENV_20M.csv
│   ├── Manual_Geno2Pheno_INT_20M.csv
│   └── Manual_Geno2Pheno_PRRT_20M.csv
├── References
│   ├── Reference_ENV_Panel_Stanford.fas
│   ├── Reference_INT_Panel_Stanford.fas
│   └── Reference_PRRT_Panel_Stanford.fas

```

A decision is made based on a combination of three publicly available subtyping tools. Records with unclear or ambiguous subtypes are sorted and concatenated with the Stanford reference panels followed by a multiple suquence alignment (msa) via Mafft. MSA samples are analysed, using IQTREE to make a final decision and respective updates.

A final output of the pipeline is an .xlsx file formatted for an internal DB and a plot. The pipeline is supposed to be used for each sequencing run of 96 samples, including control samples. 

An initial pipeline design was meant to process all three fragments (PRRT, INT, and ENV). The curresnt version of the pipeline can manage either 3 fragments or 2 (PRRT and INT), using a parameter --noenv.

![Plot](Documentation/images/MS95_subtype_counts.png)