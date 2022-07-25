#!/usr/bin/env nextflow
nextflow.enable.dsl = 2


projectDir = "/Users/vera/Learning/CQ/Internship/rki_subtyping_resistance/Subtyping"
params.comet_rest = "/Users/vera/Learning/CQ/Internship/rki_subtyping_resistance/Subtyping/comet_rest.py"
params.stanford_parser = "/Users/vera/Learning/CQ/Internship/rki_subtyping_resistance/Subtyping/stanford_parser.py"


process stanford {
  publishDir "${params.outdir}", mode: "copy", overwrite: true
  
  input:
    path fasta

  output:
    path "${fasta.getSimpleName()}.json"
  
  script:
    """
    sierrapy fasta ${fasta} -o ${fasta.getSimpleName()}.json
  
    """
}

process json_to_csv {
  publishDir "${params.outdir}/stanford", mode: "copy", overwrite: true
  input:
 
    path json
    
  output:
    path "stanford_${json.getSimpleName()}.csv"
  
  script:
   """
    python ${params.stanford_parser} ${json} stanford_${json.getSimpleName()}.csv
   """

}

process comet{
   publishDir "${params.outdir}/comet", mode: "copy", overwrite: true
  input:
    
    path fasta

  output:
    //path "comet_${fasta.getSimpleName()}_raw.csv", emit: raw
    path "comet_${fasta.getSimpleName()}.csv", emit: clean
  
  script:
  
  """
    python ${params.comet_rest} ${fasta} comet_${fasta.getSimpleName()}.csv
  """
  
}


workflow {
    inputfasta = channel.fromPath("${projectDir}/*.fasta")
    stanfordChannel = stanford(inputfasta)
    //inputpython_stanford = channel.fromPath("$projectDir/stanford_parser.py")
    //inputpython_comet = channel.fromPath("$projectDir/comet_rest.py")
    json_csvChannel = json_to_csv(stanfordChannel.flatten())
    cometChannel = comet(inputfasta.flatten())

}