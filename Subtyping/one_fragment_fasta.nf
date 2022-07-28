#!/usr/bin/env nextflow
nextflow.enable.dsl = 2


projectDir = "/Users/vera/Learning/CQ/Internship/rki_subtyping_resistance/Subtyping"
params.comet_rest = "${projectDir}/comet_rest.py"
params.stanford_parser = "${projectDir}/stanford_parser.py"


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
    python3 ${params.stanford_parser} ${json} stanford_${json.getSimpleName()}.csv
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
    python3 ${params.comet_rest} ${fasta} comet_${fasta.getSimpleName()}.csv
  """
  
}

process prrt_joint {
  publishDir "${params.outdir}", mode: "copy", overwrite: true
  input:
 
    path stanford
    path comet
    
  output:
    path "prrt_joint.csv"
  
  script:
    """
     mlr --csv join -u --ul --ur -j SequenceName -f ${stanford} ${comet} > prrt_joint.csv
    """

}

workflow {
    inputfasta = channel.fromPath("${projectDir}/*.fasta")
    stanfordChannel = stanford(inputfasta)
    //inputpython_stanford = channel.fromPath("$projectDir/stanford_parser.py")
    //inputpython_comet = channel.fromPath("$projectDir/comet_rest.py")
    json_csvChannel = json_to_csv(stanfordChannel)
    cometChannel = comet(inputfasta)
    prrt_jointChannel = prrt_joint(json_csvChannel.filter(~/.*_PRRT_20.csv$/), cometChannel.filter(~/.*_PRRT_20.csv$/))
   
}