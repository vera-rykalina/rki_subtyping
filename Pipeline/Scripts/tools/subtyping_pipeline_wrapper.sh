#!/bin/bash

#SBATCH --cpus-per-task=1
#SBATCH --time=200:00:00
#SBATCH --mem=4GB
#SBATCH --partition=long
#SBATCH --out=analyses_ba_%A.out
#SBATCH --error=analyses_ba_%A.err


nextflow Scripts/iqtree3.nf \
--outdir iqtree3 \
-c Scripts/rki_profile.config \
--projectdir /scratch/rykalinav/rki_subtyping/Pipeline \
-profile rki_slurm,rki_priority

