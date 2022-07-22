#!/usr/bin/env nextflow
nextflow.enable.dsl = 2


projectDir = "/Users/vera/Learning/CQ/Internship/rki_subtyping_resistance/Subtyping/"


process stanford {
  publishDir "${params.outdir}", mode: "copy", overwrite: true
  
  input:
    path fasta

  output:
    path "prrt.json"
  
  script:
    """
    sierrapy fasta ${fasta} -o prrt.json
  
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
    path "comet_prrt_raw.csv", emit: raw
    path "comet_prrt.csv", emit: clean

  script:

  """
   python comet_rest.py
  
  """
}


workflow {
    inputfasta = channel.fromPath(params.fasta)
    inputfasta.view()
    stanfordChannel = stanford(inputfasta)
    stanfordChannel.view()
    inputjson = channel.fromPath("${projectDir}/results/prrt.json")
    inputjson.view()
    inputpython_stanford = channel.fromPath("$projectDir/stanford_parser.py")
    inputpython_stanford.view()
    inputpython_comet = channel.fromPath("$projectDir/comet_rest.py")
    inputpython_comet.view()
    json_csvChannel = json_to_csv(inputjson, inputpython_stanford)
    json_csvChannel.view()
    cometChannel = comet(inputfasta, inputpython_comet)
    cometChannel.raw.view()
    cometChannel.clean.view()
}