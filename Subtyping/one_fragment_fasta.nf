#!/usr/bin/env nextflow
nextflow.enable.dsl = 2


project_dir = "/Users/vera/Learning/CQ/Internship/rki_subtyping_resistance/Subtyping/"


process stanford {
  publishDir "${params.outdir}", mode: "copy", overwrite: true
  
  input:
    path fastafile

  output:
    path "prrt.json"
  
  script:
    """
    sierrapy fasta ${fastafile} -o prrt.json
    """
}

process json_to_csv {
  publishDir "${params.outdir}/stanford", mode: "copy", overwrite: true
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

process comet{
   publishDir "${params.outdir}/comet", mode: "copy", overwrite: true
  input:
    path fasta
    path python

  output:
    path "comet_prrt_raw.csv"
    path "comet_prrt.csv"

  script:

  """
   python comet_rest.py
  
  """
}

workflow {
    inputfasta = channel.fromPath(params.fastafile)
    //inputfasta.view()
    stanfordChannel = stanford(inputfasta)
    //stanfordChannel.view()
    inputjson = channel.fromPath("${project_dir}/results/prrt.json")
    //inputjson.view()
    inputpython_stanford = channel.fromPath("$project_dir/stanford_parser.py")
    //inputpython_stanford.view()
    inputpython_comet = channel.fromPath("$project_dir/comet_rest.py")
    //inputpython_comet.view()
    json_csvChannel=json_to_csv(inputjson, inputpython_stanford)
    //json_csvChannel.view()
    cometChannel = comet(inputfasta, inputpython_comet)
}