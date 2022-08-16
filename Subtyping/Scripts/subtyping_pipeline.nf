#!/usr/bin/env nextflow
nextflow.enable.dsl = 2


projectDir = "/Users/vera/Learning/CQ/Internship/rki_subtyping_resistance/Subtyping"
params.comet_rest = "${projectDir}/Scripts/comet_rest.py"
params.stanford_parser = "${projectDir}/Scripts/stanford_parser.py"
params.rega_parser = "${projectDir}/Scripts/rega_parser.py"
params.tag_parser = "${projectDir}/Scripts/tag_parser.py"
params.decision = "${projectDir}/Scripts/decision.py"
params.marking = "${projectDir}/Scripts/repeat_marking.py"
params.full_join = "${projectDir}/Scripts/full_join.py"
params.report = "${projectDir}/Scripts/report.py"
params.phylo = "${projectDir}/Scripts/fasta_phylo.py"

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


process decision_to_csv {
  publishDir "${params.outdir}/with_decision", mode: "copy", overwrite: true
  input:

    path csv_prrt
    path csv_env
    path csv_int
    
  output:
    path "with_decision_${csv_prrt.getSimpleName()}.csv"
    path "with_decision_${csv_env.getSimpleName()}.csv"
    path "with_decision_${csv_int.getSimpleName()}.csv"
  
  script:
   """
    python3 ${params.decision} ${csv_prrt} with_decision_${csv_prrt.getSimpleName()}.csv
    python3 ${params.decision} ${csv_env} with_decision_${csv_env.getSimpleName()}.csv
    python3 ${params.decision} ${csv_int} with_decision_${csv_int.getSimpleName()}.csv
   """
}

process full_joint {
  publishDir "${params.outdir}/full_joint", mode: "copy", overwrite: false
  input:

    path xlsx
    
  output:
    path "full_*.xlsx"
  
  script:
   """
    python3 ${params.full_join} ${xlsx} full_*.xlsx
   """
}

process report {
  publishDir "${params.outdir}/report", mode: "copy", overwrite: true
  input:
    
    val run
    path xlsx
    
  output:
    path "${run}_subtype_uploads.xlsx"
  
  script:
   """
    python3 ${params.report} ${xlsx} _subtype_uploads.xlsx
    mv _subtype_uploads.xlsx ${run}_subtype_uploads.xlsx
    """
}

process phylo_fasta {
  publishDir "${params.outdir}/phylo_fasta", mode: "copy", overwrite: true
  input:
    
    val run
    path xlsx
    
  output:
    path "phylo_${run}_${xlsx.getSimpleName().split('_')[1]}_20M.fasta"
  
  script:
   """
    python3 ${params.phylo} ${xlsx} ${xlsx.getSimpleName()}.fasta
    mv ${xlsx.getSimpleName()}.fasta phylo_${run}_${xlsx.getSimpleName().split('_')[1]}_20M.fasta
    """
}



workflow {
    
    inputfasta = channel.fromPath("${projectDir}/InputFasta/*.fasta")
    markedfasta = mark_fasta(inputfasta)
    stanfordChannel = stanford(markedfasta)
    json_csvChannel = json_to_csv(stanfordChannel)
    inputregacsv = channel.fromPath("${projectDir}/ManualREGA/*.csv")
    rega_csvChannel = rega_to_csv(inputregacsv)
    cometChannel = comet(markedfasta)
    prrt_jointChannel = prrt_joint(json_csvChannel.filter(~/.*_PRRT_20M.csv$/), cometChannel.filter(~/.*_PRRT_20M.csv$/), rega_csvChannel.filter(~/.*_PRRT_20M.csv$/))
    env_jointChannel = env_joint(json_csvChannel.filter(~/.*_ENV_20M.csv$/), cometChannel.filter(~/.*_ENV_20M.csv$/), rega_csvChannel.filter(~/.*_ENV_20M.csv$/))
    int_jointChannel = int_joint(json_csvChannel.filter(~/.*_INT_20M.csv$/), cometChannel.filter(~/.*_INT_20M.csv$/), rega_csvChannel.filter(~/.*_INT_20M.csv$/))
    inputtagxlsx = channel.fromPath("${projectDir}/AllSeqsCO20/*.xlsx")
    tag_csvChannel = tags_to_csv(inputtagxlsx)
    decision_csvChannel = decision_to_csv(prrt_jointChannel, env_jointChannel,int_jointChannel)
    all_dfs = tag_csvChannel.concat(decision_csvChannel).collect()
    fullChannel = full_joint(all_dfs)
    /* replace Results to params.outdir */
    fullFromPathChannel = channel.fromPath("${projectDir}/Results/full_joint/*.xlsx").collect()
    report(params.run, fullFromPathChannel)
    phylo_fasta(params.run, fullFromPathChannel.flatten())
}
