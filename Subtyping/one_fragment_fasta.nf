#!/usr/bin/env nextflow

nextflow.enable.dsl = 2

process stanford {
  publishDir "${params.outdir}", mode: "copy", overwrite: true
  
  input:
    path fasta

  output:
    path "MS95_PRRT_20.json"
  
  script:
    """
    sierrapy fasta ${fasta} -o MS95_PRRT_20.json

    """
}

workflow {
    inputfasta = channel.fromPath(params.file)
    inputfasta.view()
    stanfordChannel = stanford(inputfasta)
    stanfordChannel.view()
}