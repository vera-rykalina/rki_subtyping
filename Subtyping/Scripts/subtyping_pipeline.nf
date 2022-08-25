#!/usr/bin/env nextflow
nextflow.enable.dsl = 2


projectDir = "/Users/vera/Learning/CQ/Internship/rki/Subtyping"
params.fullpipeline = false
params.comet_rest = "${projectDir}/Scripts/comet_rest.py"
params.stanford_parser = "${projectDir}/Scripts/stanford_parser.py"
params.rega = "${projectDir}/Scripts/rega_cleanup.py"
params.tag_parser = "${projectDir}/Scripts/tag_parser.py"
params.decision = "${projectDir}/Scripts/decision.py"
params.marking = "${projectDir}/Scripts/repeat_marking.py"
params.full_join = "${projectDir}/Scripts/full_join.py"
params.report = "${projectDir}/Scripts/report.py"
params.phylo = "${projectDir}/Scripts/fasta_to_phylo.py"


log.info """
VERA RYKALINA - HIV-1 GENOTYPING PIPELINE
================================================================================
projectDir       : ${projectDir}
ourdir           : ${params.outdir}
run              : ${params.run}
fasta to phylo   : ${params.phylo}

September 2022
"""


process mark_fasta {
  publishDir "${params.outdir}/marked_fasta", mode: "copy", overwrite: true
  input:
 
    path fasta
    
  output:
    path "${fasta.getSimpleName()}M.fasta"
  
  script:
   """
    python3 ${params.marking} ${fasta} ${fasta.getSimpleName()}M.fasta

   """

}


process stanford {
  publishDir "${params.outdir}/json_files", mode: "copy", overwrite: true
  
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


process clean_rega {
  publishDir "${params.outdir}/rega", mode: "copy", overwrite: true
  input:

    path csv
    
  output:
    path "rega_${csv.getSimpleName().split('_rega_')[1]}.csv"
  
  when:
    params.fullpipeline == true

  script:
   """
    python3 ${params.rega} ${csv} rega_${csv.getSimpleName().split('_rega_')[1]}.csv
   """

}



process join_prrt {
  publishDir "${params.outdir}/joint_fragmentwise", mode: "copy", overwrite: true
  input:
 
    path stanford
    path comet
    path rega
    
  output:
    path "joint_${stanford.getSimpleName().split('stanford_')[1]}.csv"
  
   when:
    params.fullpipeline == true

  script:
    """
     mlr --csv join -u --ul --ur -j SequenceName -f ${stanford} ${comet} |  mlr --csv join -u --ul --ur -j SequenceName -f ${rega} > joint_${stanford.getSimpleName().split('stanford_')[1]}.csv
    """

}

process join_env {
  publishDir "${params.outdir}/joint_fragmentwise", mode: "copy", overwrite: true
  input:
 
    path stanford
    path comet
    path rega
    
  output:
    path "joint_${stanford.getSimpleName().split('stanford_')[1]}.csv"
  
  when:
   params.fullpipeline == true
  
  script:
    """
     mlr --csv join -u --ul --ur -j SequenceName -f ${stanford} ${comet} |  mlr --csv join -u --ul --ur -j SequenceName -f ${rega} > joint_${stanford.getSimpleName().split('stanford_')[1]}.csv
    """

}

process join_int {
  publishDir "${params.outdir}/joint_fragmentwise", mode: "copy", overwrite: true
  input:
 
    path stanford
    path comet
    path rega
    
  output:
    path "joint_${stanford.getSimpleName().split('stanford_')[1]}.csv"
  
  when:
    params.fullpipeline == true

  script:
    """
     mlr --csv join -u --ul --ur -j SequenceName -f ${stanford} ${comet} | mlr --csv join -u --ul --ur -j SequenceName -f ${rega} > joint_${stanford.getSimpleName().split('stanford_')[1]}.csv
    """

}

process get_tags {
  publishDir "${params.outdir}/tags", mode: "copy", overwrite: true
  input:
    val run
    path xlsx
    
  output:
    path "tag_${run}_${xlsx.getSimpleName().split('_')[2]}_20M.csv"
  
  script:
   """
    python3 ${params.tag_parser} ${xlsx} tag_${xlsx.getSimpleName()}.csv
    mv tag_${xlsx.getSimpleName()}.csv tag_${run}_${xlsx.getSimpleName().split('_')[2]}_20M.csv
   """
}


process make_decision {
  publishDir "${params.outdir}/with_decision", mode: "copy", overwrite: true
  input:

    path csv_prrt
    path csv_env
    path csv_int
    
  output:
    path "decision_${csv_prrt.getSimpleName().split('joint_')[1]}.csv"
    path "decision_${csv_env.getSimpleName().split('joint_')[1]}.csv"
    path "decision_${csv_int.getSimpleName().split('joint_')[1]}.csv"
  
  when:
    params.fullpipeline == true

  script:
   """
    python3 ${params.decision} ${csv_prrt} decision_${csv_prrt.getSimpleName().split('joint_')[1]}.csv
    python3 ${params.decision} ${csv_env} decision_${csv_env.getSimpleName().split('joint_')[1]}.csv
    python3 ${params.decision} ${csv_int} decision_${csv_int.getSimpleName().split('joint_')[1]}.csv
   """
}

process full_joint {
  publishDir "${params.outdir}/full_joint", mode: "copy", overwrite: true
  input:
    path csv
    
  output:
    path "full_*.xlsx"
  
  when:
    params.fullpipeline == true

  script:
   """
    python3 ${params.full_join} ${csv} full_*.xlsx
   """
}

process report {
  publishDir "${params.outdir}/report", mode: "copy", overwrite: false
  input:
    path xlsx
    
  output:
    path "*.xlsx"
  
  when:
    params.fullpipeline == true

  script:
   """
    python3 ${params.report} ${xlsx} *.xlsx
    """
}

process phylo_fasta {
  publishDir "${params.outdir}/phylo_fasta", mode: "copy", overwrite: true
  input:
    
    val run
    path xlsx
    
  output:
    path "phylo_${run}_${xlsx.getSimpleName().split('_')[2]}_20M.fasta"
  
  when:
    params.fullpipeline == true

  script:
   """
    python3 ${params.phylo} ${xlsx} ${xlsx.getSimpleName()}.fasta
    mv ${xlsx.getSimpleName()}.fasta phylo_${run}_${xlsx.getSimpleName().split('_')[2]}_20M.fasta
    """
}



workflow {
    
    inputfasta = channel.fromPath("${projectDir}/InputFasta/*.fasta")
    markedfasta = mark_fasta(inputfasta)
    stanfordChannel = stanford(markedfasta)
    json_csvChannel = json_to_csv(stanfordChannel)
    inputregacsv = channel.fromPath("${projectDir}/ManualREGA/*.csv")
    rega_csvChannel = clean_rega(inputregacsv)
    cometChannel = comet(markedfasta)
    prrt_jointChannel = join_prrt(json_csvChannel.filter(~/.*_PRRT_20M.csv$/), cometChannel.filter(~/.*_PRRT_20M.csv$/), rega_csvChannel.filter(~/.*_PRRT_20M.csv$/))
    env_jointChannel = join_env(json_csvChannel.filter(~/.*_ENV_20M.csv$/), cometChannel.filter(~/.*_ENV_20M.csv$/), rega_csvChannel.filter(~/.*_ENV_20M.csv$/))
    int_jointChannel = join_int(json_csvChannel.filter(~/.*_INT_20M.csv$/), cometChannel.filter(~/.*_INT_20M.csv$/), rega_csvChannel.filter(~/.*_INT_20M.csv$/))
    inputtagxlsx = channel.fromPath("${projectDir}/AllSeqsCO20/*.xlsx")
    tag_csvChannel = get_tags(params.run, inputtagxlsx)
    decision_csvChannel = make_decision(prrt_jointChannel, env_jointChannel,int_jointChannel)
    all_dfs = tag_csvChannel.concat(decision_csvChannel).collect()
    fullChannel = full_joint(all_dfs)
    phylo_fasta(params.run, fullChannel.flatten())
    /* replace Results to params.outdir */
    fullFromPathChannel = channel.fromPath("${projectDir}/Results/full_joint/*.xlsx").collect()
    report(params.run, fullFromPathChannel)
}
