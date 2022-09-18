# HIV-1 Subtyping

The aim of a pipeline is to automate a routine HIV-1 subtyping analysis, using Stanford (SierraPy), Comet (Rest API), and Rega (manually generated .csv files via click or drop) tools. The pipeline is built with Nextflow and custom Python scripts. Inputs of the pipeline include:

- .fasta files (fused PRRT, INT, and ENV)
- .xlsx files (NGS pipeline, contain information for invalid sequences)
- .csv files (manually generated, using Rega online tool; input: marked .fasta files)
- .fasta files of reference panels (subtype_origin_year_accession)
  
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
├── References
│   ├── Reference_ENV_Panel_Stanford.fas
│   ├── Reference_INT_Panel_Stanford.fas
│   └── Reference_PRRT_Panel_Stanford.fas
├── Scripts
│   ├── comet_rest.py
│   ├── decision.py
│   ├── fasta_for_mafft.py
│   ├── full_join.py
│   ├── json_parser.py
│   ├── nexflow.config
│   ├── plot.py
│   ├── rega_cleanup.py
│   ├── repeat_marking.py
│   ├── report.py
│   ├── subtyping_pipeline.nf
│   └── tag_parser.py
```

A decision is made based on a combination of three publicly available subtyping tools. Records with unclear or ambiguous subtypes are sorted and concatenated with the Stanford reference panels followed by a multiple suquence alignment (msa) via Mafft. MSA samples are analysed, using IQTREE to make a final decision and respective updates.

A final output of the pipeline is an .xlsx file formatted for an internal DB and a plot. The pipeline is supposed to be used for each sequencing run of 96 samples, including control samples. 

![Plot](Documentation/images/MS95_subtype_counts.png)