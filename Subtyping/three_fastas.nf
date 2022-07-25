#!/usr/bin/env nextflow
nextflow.enable.dsl = 2


projectDir = "/Users/vera/Learning/CQ/Internship/rki_subtyping_resistance/Subtyping"

include { produce_csv } from "/Users/vera/Learning/CQ/Internship/rki_subtyping_resistance/Subtyping/one_fragment_fasta.nf"

params.outdir = null

workflow{
 fastafile = channel.fromPath("${projectDir}/*.fasta").flatten()
 produce_csv(fastafile)
}