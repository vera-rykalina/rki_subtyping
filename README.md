# HIV-1 Subtyping

An aim of the project was to automate a routine HIV-1 subtyping analysis, using Stanford (SierraPy), Comet (Rest API), and Rega (manually generated .csv files via click or drop file) tools. A pipeline is built with NextFlow with custom Python scripts. Inputs of the pipeline include (mock data, imitating real datasets):

- fasta file per fragment (fused PRRT, INT, and ENV)
- .xlsx per fragment (NGS pipeline, contrain information for invalid sequences)
- manually derived .csv for Rega (using fasta files with marked repeated samples, if any)
- per fragment reference panels (subtype_origin_year_accession)
  
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
│   ├── manual_rega_MS95_ENV_20M.csv
│   ├── manual_rega_MS95_INT_20M.csv
│   └── manual_rega_MS95_PRRT_20M.csv
├── References
│   ├── Reference_ENV_Panel_Stanford.fas
│   ├── Reference_INT_Panel_Stanford.fas
│   └── Reference_PRRT_Panel_Stanford.fas
```

A decision is made based on combination of 3 subtyping tools. Records with unclear or ambiguous subtypes are sorted concatenated with the Stanford reference panels and subjected to multiple suquence alignment (msa) via Mafft. MSA samples are analysed using iQtree to make a final decision and update report table and plot.  

A final output of the pipeline .xlsx table for internal DB and a plot. The pipeline is supposed to be run for each sequencing ran of 96 samples, including control samples. 

![Plot](Documentation/images/MS95_subtype_counts.png)