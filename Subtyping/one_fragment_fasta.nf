#!/usr/bin/env nextflow

project_dir = "/Users/vera/Learning/CQ/Internship/rki_subtyping_resistance/Subtyping/"
stanford_dir = "/Users/vera/Learning/CQ/Internship/rki_subtyping_resistance/Subtyping/stanford/"

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

process json_to_csv {
  publishDir "${params.outdir}", mode: "copy", overwrite: true
  input:
    path json
    path python

  output:
    path "stanford_prrt.csv"

  script:
  """
   python stanford_parser.py

  """

}

workflow {
    inputfasta = channel.fromPath(params.file)
    inputfasta.view()
    stanfordChannel = stanford(inputfasta)
    stanfordChannel.view()
    inputjson = channel.fromPath("${stanford_dir}/*.json")
    inputjson.view()
    inputpython = channel.fromPath("$project_dir/stanford_parser.py")
    inputpython.view()
    jsonChannel=json_to_csv(inputjson, inputpython)
    jsonChannel.view()
}