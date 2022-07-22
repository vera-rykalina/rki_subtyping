#!/usr/bin/env nextflow
nextflow.enable.dsl = 2

process stanford {
  publishDir "${params.outdir}", mode: "copy", overwrite: true
  
  input:
    path fastafiles

  output:
    path "${fastafile}.json"
  
  script:
    """
    sierrapy fasta ${fastafiles} -o ${fastafile}.json
  
    """
}