#!/bin/bash

#SBATCH --cpus-per-task=4
#SBATCH --time=120:00:00
#SBATCH --mem=25GB
#SBATCH --partition=main
#SBATCH --out=analyses_ba_%A.out
#SBATCH --error=analyses_ba_%A.err


 iqtree \
      -s msa_VALIDATION_FL_checked.fasta \
      -m GTR+I+G4 \
      -B 5000 \
      -nm 5000 \
      -T 4 \
      -cptime 3600 \
      --prefix iqtree_VALIDATION_FL

# A special option -nt AUTO will tell IQ-TREE to automatically determine the best number of cores
# given the current data and computer.