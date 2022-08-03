#!/usr/bin/env nextflow
nextflow.enable.dsl = 2


projectDir = "/Users/vera/Learning/CQ/Internship/rki_subtyping_resistance/Subtyping"
params.comet_rest = "${projectDir}/Scripts/comet_rest.py"
params.stanford_parser = "${projectDir}/Scripts/stanford_parser.py"
params.rega_parser = "${projectDir}/Scripts/rega_parser.py"
params.tag_parser = "${projectDir}/Scripts/tag_parser.py"


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
    path "comet_${fasta.getSimpleName()}.csv"
  
  script:
  
  """
    python3 ${params.comet_rest} ${fasta} comet_${fasta.getSimpleName()}.csv
  """
  
}


process rega_to_csv {
  publishDir "${params.outdir}/rega", mode: "copy", overwrite: true
  input:

    path csv
    
  output:
    path "rega_${csv.getSimpleName()}.csv"
  
  script:
   """
    python3 ${params.rega_parser} ${csv} rega_${csv.getSimpleName()}.csv
   """

}



process prrt_joint {
  publishDir "${params.outdir}/joint_fragmentwise", mode: "copy", overwrite: true
  input:
 
    path stanford
    path comet
    path rega
    
  output:
    path "PRRT_joint.csv"
  
  script:
    """
     mlr --csv join -u --ul --ur -j SequenceName -f ${stanford} ${comet} |  mlr --csv join -u --ul --ur -j SequenceName -f ${rega} > PRRT_joint.csv
    """

}

process env_joint {
  publishDir "${params.outdir}/joint_fragmentwise", mode: "copy", overwrite: true
  input:
 
    path stanford
    path comet
    path rega
    
  output:
    path "ENV_joint.csv"
  
  script:
    """
     mlr --csv join -u --ul --ur -j SequenceName -f ${stanford} ${comet} |  mlr --csv join -u --ul --ur -j SequenceName -f ${rega} > ENV_joint.csv
    """

}

process int_joint {
  publishDir "${params.outdir}/joint_fragmentwise", mode: "copy", overwrite: true
  input:
 
    path stanford
    path comet
    path rega
    
  output:
    path "INT_joint.csv"
  
  script:
    """
     mlr --csv join -u --ul --ur -j SequenceName -f ${stanford} ${comet} | mlr --csv join -u --ul --ur -j SequenceName -f ${rega} > INT_joint.csv
    """

}

process tags_to_csv {
  publishDir "${params.outdir}/tagged_seqs", mode: "copy", overwrite: true
  input:

    path xlsx
    
  output:
    path "tagged_${xlsx.getSimpleName()}.csv"
  
  script:
   """
    python3 ${params.tag_parser} ${xlsx} tagged_${xlsx.getSimpleName()}.csv
   """

}


workflow {
    inputfasta = channel.fromPath("${projectDir}/InputFasta/*.fasta")
    stanfordChannel = stanford(inputfasta)
    json_csvChannel = json_to_csv(stanfordChannel)
    inputregacsv = channel.fromPath("${projectDir}/ManualREGA/*.csv")
    rega_csvChannel = rega_to_csv(inputregacsv)
    cometChannel = comet(inputfasta)
    prrt_jointChannel = prrt_joint(json_csvChannel.filter(~/.*_PRRT_20.csv$/), cometChannel.filter(~/.*_PRRT_20.csv$/), rega_csvChannel.filter(~/.*_PRRT_20.csv$/))
    env_jointChannel = env_joint(json_csvChannel.filter(~/.*_ENV_20.csv$/), cometChannel.filter(~/.*_ENV_20.csv$/), rega_csvChannel.filter(~/.*_ENV_20.csv$/))
    int_jointChannel = int_joint(json_csvChannel.filter(~/.*_INT_20.csv$/), cometChannel.filter(~/.*_INT_20.csv$/), rega_csvChannel.filter(~/.*_INT_20.csv$/))
    inputtagxlsx = channel.fromPath("${projectDir}/AllSeqsCO20/*.xlsx")
    tag_csvChannel = tags_to_csv(inputtagxlsx)

}