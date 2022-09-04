---
marp: true
paginate: true
author: Vera Rykalina
theme: default
size: 4:3
footer: Vera Rykalina | September 2022

---

# SUBTYPING PIPELINE

---
## Contents

> Quick Guide

> Supplementary

> Conda

> GitHub Repo 
---

# Quick Guide
---

## Pipeline Directory
Locate to Pipeline directory:
```sh
$ cd ~/rki_subtyping/Pipeline
```
Open IDE
```sh
$ code ../
```
---
## Input Folders
Make sure you have 5 directories:

```sh
tree  -d
```

```sh
├── AllSeqsCO20
├── InputFasta
├── ManualRega
├── References
└── Scripts
```

---
## AllSeqCO20 Folder
Prodive this folder with .xlsx files as listed (from NGS pipeline): 
```sh
AllSeqsCO20/
├── MS95_Seqs_ENV_CO20_V5.xlsx
├── MS95_Seqs_INT_CO20_V5.xlsx
└── MS95_Seqs_PRRT_CO20_V5.xlsx
```

---
## InputFasta Folder
Prodive this folder with files as listed (from NGS pipeline): 
```sh
InputFasta/
├── MS95_ENV_20.fasta
├── MS95_INT_20.fasta
└── MS95_PRRT_20.fasta
```
---



## Activate Environment
Activate `subtyping_pipeline` environment.
```sh
$ conda activate subtyping_pipeline
```
Be sure you have change in prompt:

```sh
(subtyping_pipeline) beast2@Beast2:~/rki_sybtyping/Pipeline$
```
---
## Run Pipeline
```sh
$ nextflow Scripts/subtyping_pipeline.nf --outdir Results
``` 
You should get similar output:
```sh
N E X T F L O W  ~  version 22.04.5
Launching `Scripts/subtyping_pipeline.nf` [sleepy_jones] DSL2 - revision: 8d00da039e
[70/324dec] process > mark_fasta (1)    [100%] 3 of 3 ✔
[92/cefb1b] process > get_tags (1)      [100%] 3 of 3 ✔
[fb/23e4dd] process > comet (3)         [100%] 3 of 3 ✔
[0a/833697] process > stanford (3)      [100%] 3 of 3 ✔
[01/ca575f] process > json_to_csv (3)   [100%] 3 of 3 ✔
```

---
#### Processes Overview
```sh
[1b/f2f10a] process > mark_fasta (2)        [100%] 3 of 3, cached: 3 ✔
[73/a28f41] process > stanford (3)          [100%] 3 of 3, cached: 3 ✔
[e6/e4af1d] process > json_to_csv (3)       [100%] 3 of 3, cached: 3 ✔
[65/e0eb90] process > clean_rega (3)        [100%] 3 of 3, cached: 3 ✔
[97/70bbdd] process > comet (3)             [100%] 3 of 3, cached: 3 ✔
[62/e59285] process > join_prrt (1)         [100%] 1 of 1, cached: 1 ✔
[87/4d2fcf] process > join_env (1)          [100%] 1 of 1, cached: 1 ✔
[34/36991e] process > join_int (1)          [100%] 1 of 1, cached: 1 ✔
[a9/dd644a] process > get_tags (3)          [100%] 3 of 3, cached: 3 ✔
[8d/dad394] process > make_decision (1)     [100%] 1 of 1, cached: 1 ✔
[d8/983216] process > join_with_tags        [100%] 1 of 1, cached: 1 ✔
[e6/ceaa42] process > fasta_for_mafft (2)   [100%] 3 of 3, cached: 3 ✔
[f7/9e1ccf] process > prrt_concat_panel (1) [100%] 1 of 1, cached: 1 ✔
[a4/b7aaee] process > int_concat_panel (1)  [100%] 1 of 1, cached: 1 ✔
[54/89322b] process > env_concat_panel (1)  [100%] 1 of 1  cached: 1 ✔
[c0/786bcd] process > mafft (3)             [100%] 3 of 3, cached: 2 ✔
[68/72f0eb] process > iqtree (3)            [100%] 3 of 3 ✔
[3c/0fb71f] process > report                [100%] 1 of 1, cached: 1 ✔
[c5/462a18] process > countplot (1)         [100%] 1 of 1, cached: 1 ✔
```
---
# Supplementary
---

## Example of .fasta within InputFasta
```sh
>20-02955_ENV_20
GGAATTAGGCCAGTGGTGTCAACCCAACTATTGTTAAATGGCAGCCTAGCAGAAGAAGAT
GTGGTCATTAGATCTGAAAATTTCACAAACAATGCTAAAACCATAATAGTACAGCTTAAT
GAAACAGTAGTGATTAATTGTACAAGACCCGGCAACAATACAAGAAAAAGTATACATATA
GGACCAGGAAAAGCATGGTATGCAACAGGAGAGATAATAGGAGATATAAGACAAGCACAT
TGTAAACTTAATAAAACACAATGGGAAAAAACTTTAAAAAGGGTAGCTAGTAAATTAAGG
AAACAATCCAACCTTACAACAGTAATCTTTAAGAACTCCTCAGGGGGGGACCCAGAAATT
GTAATGCACAGTTTTAACTGTGGAGGGGAATTTTTCTATTGTAACACAACACAGTTGTTC
AATAGTATTTGGAATGACACTACTAATAGTACTGACACAAATGAAACTATCACACTCCCA
TGCAGAATAAAACAAATTATAAATAGATGGCAGGAAGCAGGAAGGG
```
---
## Example of .xlsx within AllSeqsCO20
```
Scount	        Fragment    Cutoff  Header	        Lauf   NGS-ID	Index GenBank-ID Sequenz
20-02944	PRRT	    20	    20-02944_PRRT_20	95	   	1	         CCCCT...
20-02945	PRRT	    20	    20-02945_PRRT_20	95	  	2	         CCCCT...
20-02947	PRRT	    20	    20-02947_PRRT_20	95	        3	         CCCCT...
20-02949	PRRT	    20	    20-02949_PRRT_20	95	        4	         CCCCT...
20-02950	PRRT	    20	    20-02950_PRRT_20	95	   	5	         CCCCT...
```
---
## References Folder
This folder contains reference panels and does not need any change unless reference panels should be replaced.   
```sh
References/
├── Reference_ENV_Panel_Stanford.fas
├── Reference_INT_Panel_Stanford.fas
└── Reference_PRRT_Panel_Stanford.fas
```
---

## Scripts Folder
This folder contains the scripts and does not need any change. 
```sh
Scripts/
├── comet_rest.py
├── decision.py
├── fasta_for_mafft.py
├── full_join.py
├── json_parser.py
├── nexflow.config
├── plot.py
├── rega_cleanup.py
├── repeat_marking.py
├── report.py
├── subtyping_pipeline.nf
└── tag_parser.py
```
---
# Conda

---
## Conda Info
List available conda environments.
```sh
$ conda info --envs
# conda environments:
#
base                  *  /home/beast2/anaconda3
subtyping_pipeline       /home/beast2/anaconda3/envs/subtyping_pipeline
```
---
## Conda Version
Pipeline's version of conda `4.14.0`
```sh
$ conda --version
```
---

## Deactivation of Environment
This command is used to deactivate the current invironment.
```sh
$ conda deactivate
```
Be sure you have change in prompt:

```sh
(base) beast2@Beast2:~/rki_sybtyping/Pipeline$
```

---
# GitHub Repo

---
## Repo Link 
The project is hosted [here](https://github.com/vera-rykalina/rki_subtyping).  Use this link to clone the repo in case of data loss.

---

## How to Clone
Locate to home directory
```sh
$ cd
```
Clone the repo 
```sh
$ git clone https://github.com/vera-rykalina/rki_subtyping
```
Modify path of `ProjectDir` within `subtyping_pipeline.nf`

```sh
projectDir = "/home/beast3/rki_subtyping/Pipeline 
```




