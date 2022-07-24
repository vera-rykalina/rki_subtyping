#!/usr/bin/env nextflow
nextflow.enable.dsl = 2


projectDir = "/Users/vera/Learning/CQ/Internship/rki_subtyping_resistance/Subtyping/"


process stanford {
  publishDir "${params.outdir}", mode: "copy", overwrite: true
  
  input:
    path fastafile

  output:
    path "${fastafile.getSimpleName()}.json"
  
  script:
    """
    sierrapy fasta ${fastafile} -o ${fastafile.getSimpleName()}.json
  
    """
}

process json_to_csv {
  publishDir "${params.outdir}/stanford", mode: "copy", overwrite: true
  input:
    path json
    path python

  output:
    path "stanford_${json.getSimpleName()}.csv"
  
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

    //path "comet_${fasta.getSimpleName()}_raw.csv", emit: raw
    path "comet_${fasta.getSimpleName()}.csv", emit: clean
  
  script:

  """
   python comet_rest.py
  
  """
}


workflow {
    inputfasta = channel.fromPath(params.fastafile)
    inputfasta.view()
    stanfordChannel = stanford(inputfasta)
    stanfordChannel.view()
    //inputjson = channel.fromPath("${projectDir}/params.outdir/*.json")
    //inputjson.view()
    inputpython_stanford = channel.fromPath("$projectDir/stanford_parser.py")
    //inputpython_stanford.view()
    inputpython_comet = channel.fromPath("$projectDir/comet_rest.py")
    //inputpython_comet.view()
    json_csvChannel = json_to_csv(stanfordChannel, inputpython_stanford)
    json_csvChannel.view()
    cometChannel = comet(inputfasta, inputpython_comet)
    //cometChannel.raw.view()
    cometChannel.clean.view()
}