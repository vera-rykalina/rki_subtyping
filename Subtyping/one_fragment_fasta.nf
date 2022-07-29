#!/usr/bin/env nextflow
nextflow.enable.dsl = 2


projectDir = "/Users/vera/Learning/CQ/Internship/rki_subtyping_resistance/Subtyping"
params.comet_rest = "${projectDir}/comet_rest.py"
params.stanford_parser = "${projectDir}/stanford_parser.py"
params.rega_parser = "${projectDir}/rega_parser.py"

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
    
  output:
    path "prrt_joint.csv"
  
  script:
    """
     mlr --csv join -u --ul --ur -j SequenceName -f ${stanford} ${comet} > prrt_joint.csv
    """

}

process env_joint {
  publishDir "${params.outdir}/joint_fragmentwise", mode: "copy", overwrite: true
  input:
 
    path stanford
    path comet
    
  output:
    path "env_joint.csv"
  
  script:
    """
     mlr --csv join -u --ul --ur -j SequenceName -f ${stanford} ${comet} > env_joint.csv
    """

}

process int_joint {
  publishDir "${params.outdir}/joint_fragmentwise", mode: "copy", overwrite: true
  input:
 
    path stanford
    path comet
    
  output:
    path "int_joint.csv"
  
  script:
    """
     mlr --csv join -u --ul --ur -j SequenceName -f ${stanford} ${comet} > int_joint.csv
    """

}

process prrt_joint_rega {
  publishDir "${params.outdir}/joint_stf_com_reg", mode: "copy", overwrite: true
  input:
 
    path joint
    path rega
    
  output:
    path "prrt_full_join.csv"
  
  script:
    """
     mlr --csv join -u --ul --ur -j SequenceName -f ${joint} ${rega} > prrt_full_join.csv
    """

}

process int_joint_rega {
  publishDir "${params.outdir}/joint_stf_com_reg", mode: "copy", overwrite: true
  input:
 
    path joint
    path rega
    
  output:
    path "int_full_join.csv"
  
  script:
    """
     mlr --csv join -u --ul --ur -j SequenceName -f ${joint} ${rega} > int_full_join.csv
    """

}

process env_joint_rega {
  publishDir "${params.outdir}/joint_stf_com_reg", mode: "copy", overwrite: true
  input:
 
    path joint
    path rega
    
  output:
    path "env_full_join.csv"
  
  script:
    """
     mlr --csv join -u --ul --ur -j SequenceName -f ${joint} ${rega} > env_full_join.csv
    """

}


workflow {
    inputfasta = channel.fromPath("${projectDir}/*.fasta")
    stanfordChannel = stanford(inputfasta)
    //inputpython_stanford = channel.fromPath("$projectDir/stanford_parser.py")
    //inputpython_comet = channel.fromPath("$projectDir/comet_rest.py")
    json_csvChannel = json_to_csv(stanfordChannel)
    inputregacsv = channel.fromPath("${projectDir}/*.csv")
    rega_csvChannel = rega_to_csv(inputregacsv)
    cometChannel = comet(inputfasta)
    prrt_jointChannel = prrt_joint(json_csvChannel.filter(~/.*_PRRT_20.csv$/), cometChannel.filter(~/.*_PRRT_20.csv$/))
    env_jointChannel = env_joint(json_csvChannel.filter(~/.*_ENV_20.csv$/), cometChannel.filter(~/.*_ENV_20.csv$/))
    int_jointChannel = int_joint(json_csvChannel.filter(~/.*_INT_20.csv$/), cometChannel.filter(~/.*_INT_20.csv$/))

    prrtfullChannel = prrt_joint_rega(prrt_jointChannel.filter(~/.*prrt_joint.csv$/), rega_csvChannel.filter(~/.*_PRRT_20.csv$/))
    envfullChannel = env_joint_rega(env_jointChannel.filter(~/.*env_joint.csv$/), rega_csvChannel.filter(~/.*_ENV_20.csv$/))
    intfullChannel = int_joint_rega(int_jointChannel.filter(~/.*int_joint.csv$/), rega_csvChannel.filter(~/.*_INT_20.csv$/))
}