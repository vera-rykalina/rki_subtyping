nextflow.enable.dsl = 2

// help message
params.help = false

if (params.help) { exit 0, helpMSG() }

def helpMSG() {
    c_green = "\033[0;32m";
    c_reset = "\033[0m";
    c_yellow = "\033[0;33m";
    c_blue = "\033[0;34m";
    c_red = "\u001B[31m";
    c_dim = "\033[2m";
    log.info """
  

    ${c_blue}HIVtype${c_blue}
    =================================================================================================================
    Author: Vera Rykalina
    ${c_blue}Affiliation: Robert Koch Institute${c_blue}
    =================================================================================================================
  

    ${c_yellow}Usage example:${c_reset}
    nextflow hivtype.nf -c hivtype.config --full --iqtree --report -profile profile --oudir output
   
    
    ${c_green}Options:${c_reset}  

    --noenv             Add this option if there are no ENV fragment (PRRT and INT only)

    --full              Add this option to run the pipeline up to MSA the via MAFFT (otherwise the first 5 processes)
 
    --iqtree            Add this option to start building trees 

    --rkireport         Add this option to generate a report (column names are in German)

    --withxlsx          Add this option if there are AllSeqCO20 xlsx files (produced by the HIVpipe pipeline) 
    
    --outdir            Name for an output directory e.g. output [string]

    """
}


params.noenv = false
params.full = false
params.iqtree = false
params.withxlsx = false
params.rkireport = false

params.outdir = null
if (!params.outdir) {
  println "outdir: $params.outdir"
  error "Missing output directory!"
}

params.profile = null
if (params.profile) {
  exit 1, "--profile is WRONG use -profile"
}


log.info """
VERA RYKALINA - HIV-1 SUBTYPING PIPELINE
================================================================================
projectDir            : ${projectDir}
outdir                : ${params.outdir}
withxlsx              : ${params.withxlsx}
full                  : ${params.full}
iqtree                : ${params.iqtree}
noenv                 : ${params.noenv}
rkireport             : ${params.rkireport}

"""


process mark_fasta {
  publishDir "${params.outdir}/1_marked_fasta", mode: "copy", overwrite: true
  input:
 
    path fasta
    
  output:
    path "${fasta.getSimpleName()}M.fasta"
  
  script:
   """
    repeat_marking.py ${fasta} ${fasta.getSimpleName()}M.fasta

   """

}

process get_tags {
  publishDir "${params.outdir}/2_tags", mode: "copy", overwrite: true
  input:
    path xlsx
    
  output:
    path "tag_${xlsx.getSimpleName().split('_')[0]}_${xlsx.getSimpleName().split('_')[2]}_20M.csv"

  script:
   """
   tag_parser.py ${xlsx} tag_${xlsx.getSimpleName().split('_')[0]}_${xlsx.getSimpleName().split('_')[2]}_20M.csv
   """
}
process comet {
   publishDir "${params.outdir}/3_comet", mode: "copy", overwrite: true
  input:
    
    path fasta

  output:
    path "comet_${fasta.getSimpleName()}.csv"

  script:
  
  """
  comet_rest.py ${fasta} comet_${fasta.getSimpleName()}.csv
  """
  
}


process stanford {
  publishDir "${params.outdir}/4_json_files", mode: "copy", overwrite: true
  
  input:
    path fasta_gql
    //fasta_gql[0] fasta
    //fasta_gql[1] gql

  output:
    path "${fasta_gql[0].getSimpleName()}.json"
  

  script:
    """
    sierrapy fasta ${fasta_gql[0]} --no-sharding -q ${fasta_gql[1]} -o ${fasta_gql[0].getSimpleName()}.json
  
    """
}

process json_to_csv {
  publishDir "${params.outdir}/5_stanford", mode: "copy", overwrite: true
  input:
 
    path json
    
  output:
    path "stanford_${json.getSimpleName()}.csv"
  
  script:
   """
   json_parser.py ${json} stanford_${json.getSimpleName()}.csv
   """

}


process g2p {
  publishDir "${params.outdir}/6_g2p", mode: "copy", overwrite: true
  input:

    path csv
    
  output:
    path "g2p_${csv.getSimpleName().split('_Geno2Pheno_')[1]}.csv"
  
  when:
    params.full == true

  script:
   """
   geno2pheno.py ${csv} g2p_${csv.getSimpleName().split('_Geno2Pheno_')[1]}.csv
   """

}

process clean_rega {
  publishDir "${params.outdir}/7_rega", mode: "copy", overwrite: true
  input:

    path csv
    
  output:
    path "rega_${csv.getSimpleName().split('_Rega_')[1]}.csv"
  
  when:
    params.full == true

  script:
   """
   rega_cleanup.py ${csv} rega_${csv.getSimpleName().split('_Rega_')[1]}.csv
   """
}


process join_prrt {
  publishDir "${params.outdir}/8_joint_fragmentwise", mode: "copy", overwrite: true
  input:
 
    path stanford
    path comet
    path g2p
    path rega
    
  output:
    path "joint_${comet.getSimpleName().split('comet_')[1]}.csv"
  
   when:
    params.full == true

  script:
    """
     mlr \
      --csv join \
      -u \
      --ul \
      --ur \
      -j SequenceName \
      -f ${stanford} ${comet} |\
      mlr --csv join -u --ul --ur -j SequenceName -f ${g2p} |\
      mlr --csv join -u --ul --ur -j SequenceName -f ${rega} > joint_${comet.getSimpleName().split('comet_')[1]}.csv
    """

}

process join_env {
  publishDir "${params.outdir}/8_joint_fragmentwise", mode: "copy", overwrite: true
  input:
 
    path comet
    path g2p
    path rega
    
  output:
    path "joint_${comet.getSimpleName().split('comet_')[1]}.csv"
  
  when:
   params.full == true
  
  script:
    """
     mlr \
      --csv join \
      -u \
      --ul \
      --ur \
      -j SequenceName -f ${g2p} ${comet} |\
      mlr --csv join -u --ul --ur -j SequenceName -f ${rega} > joint_${comet.getSimpleName().split('comet_')[1]}.csv
    """

}

process join_int {
  publishDir "${params.outdir}/8_joint_fragmentwise", mode: "copy", overwrite: true
  input:
 
    path stanford
    path comet
    path g2p
    path rega
    
  output:
    path "joint_${comet.getSimpleName().split('comet_')[1]}.csv"
  
  when:
    params.full == true

  script:
    """
     mlr \
      --csv join \
      -u \
      --ul \
      --ur \
      -j SequenceName \
      -f ${stanford} ${comet} |\
      mlr --csv join -u --ul --ur -j SequenceName -f ${g2p} |\
      mlr --csv join -u --ul --ur -j SequenceName -f ${rega} > joint_${comet.getSimpleName().split('comet_')[1]}.csv
    """

}


process make_decision {
  publishDir "${params.outdir}/9_with_decision", mode: "copy", overwrite: true
  input:

    path csv_prrt
    path csv_env
    path csv_int
    
  output:
    path "decision_${csv_prrt.getSimpleName().split('joint_')[1]}.csv"
    path "decision_${csv_env.getSimpleName().split('joint_')[1]}.csv"
    path "decision_${csv_int.getSimpleName().split('joint_')[1]}.csv"
  
  when:
    params.full == true

  script:
   """
    decision.py ${csv_prrt} decision_${csv_prrt.getSimpleName().split('joint_')[1]}.csv
    decision.py ${csv_env} decision_${csv_env.getSimpleName().split('joint_')[1]}.csv
    decision.py ${csv_int} decision_${csv_int.getSimpleName().split('joint_')[1]}.csv
   """
}

process make_decision_no_env {
  publishDir "${params.outdir}/9_with_decision", mode: "copy", overwrite: true
  input:

    path csv_prrt
    path csv_int
    
  output:
    path "decision_${csv_prrt.getSimpleName().split('joint_')[1]}.csv"
    path "decision_${csv_int.getSimpleName().split('joint_')[1]}.csv"
  
  when:
    params.full == true

  script:
   """
    decision.py ${csv_prrt} decision_${csv_prrt.getSimpleName().split('joint_')[1]}.csv
    decision.py ${csv_int} decision_${csv_int.getSimpleName().split('joint_')[1]}.csv
   """
}



process xlsx2fragments {
  publishDir "${params.outdir}/0_xlsx", mode: "copy", overwrite: true
  
  input:
    path fasta_prrt
    path fasta_int
    
  output:
    path "*.xlsx"
  
  when: 
   // params.full == true

  script:
    """
    xlsx2fragments.py \
      -p ${fasta_prrt} \
      -i ${fasta_int} \
      -n ${fasta_prrt.getSimpleName().split('_')[0]}
     """
}

process xlsx3fragments {
  publishDir "${params.outdir}/0_xlsx", mode: "copy", overwrite: true
  
  input:
    path fasta_prrt
    path fasta_int
    path fasta_env
    
  output:
    path "*.xlsx"
  
  when: 
   // params.full == true
  
  script:
    """
    xlsx3fragments.py \
      -p ${fasta_prrt} \
      -i ${fasta_int} \
      -e ${fasta_env} \
      -n ${fasta_prrt.getSimpleName().split('_')[0]}
   """
}

process join_with_tags {
  publishDir "${params.outdir}/10_joint_with_tags", mode: "copy", overwrite: false
  input:
    path csv
    
  output:
    path "full_*.xlsx"
  
  when:
    params.full == true

  script:
   """
    full_join.py ${csv} full_*.xlsx
   """
}

process join_with_tags_no_env {
  publishDir "${params.outdir}/10_joint_with_tags", mode: "copy", overwrite: false
  input:
    path csv
    
  output:
    path "full_*.xlsx"
  
  when:
    params.full == true

  script:
   """
    full_join_no_env.py ${csv} full_*.xlsx
   """
}

process fasta_for_mafft {
  publishDir "${params.outdir}/11_fasta_for_mafft", mode: "copy", overwrite: true
  input:
    
    path xlsx
    
  output:
    
    path "*.fasta"

  when:
    params.full == true

  script:
    """
    fasta_for_mafft.py ${xlsx} *.fasta
    """
}


  process prrt_concat_panel {
  publishDir "${params.outdir}/12_concat_with_panel", mode: "copy", overwrite: true
  input:
    path fragment
    path ref

  output:
    path "concat_${fragment.getSimpleName().split('mafft_')[1]}.fasta"
  when:
    params.full == true

  script:
    """
    cat ${fragment} ${ref} > concat_${fragment.getSimpleName().split('mafft_')[1]}.fasta 
    """ 
    
  } 

  process int_concat_panel {
  publishDir "${params.outdir}/12_concat_with_panel", mode: "copy", overwrite: true
  input:
    path fragment
    path ref

  output:
      path "concat_${fragment.getSimpleName().split('mafft_')[1]}.fasta"
  when:
    params.full == true

  script:
    """
    cat ${fragment} ${ref} > concat_${fragment.getSimpleName().split('mafft_')[1]}.fasta 
    """ 
    
  } 

  process env_concat_panel {
  publishDir "${params.outdir}/12_concat_with_panel", mode: "copy", overwrite: true
  input:
    path fragment
    path ref

  output:
    path "concat_${fragment.getSimpleName().split('mafft_')[1]}.fasta"
  when:
    params.full == true

  script:
    """
    cat ${fragment} ${ref} > concat_${fragment.getSimpleName().split('mafft_')[1]}.fasta 
    """  
  } 

  process mafft {
  publishDir "${params.outdir}/13_mafft", mode: "copy", overwrite: false
  input:
      path fasta
  output:
      path  "msa_${fasta.getSimpleName().split('concat_')[1]}.fasta"

  when:
    params.full == true

  script:
  
    """
    mafft --auto ${fasta} > msa_${fasta.getSimpleName().split('concat_')[1]}.fasta
    """
  }

process iqtree {
  label "iqtree"
  publishDir "${params.outdir}/14_iqtree", mode: "copy", overwrite: true
  input:
      path fasta
  output:
      path  "*.treefile"
      path  "*.iqtree"
      path  "*.log"

  when:
    params.iqtree == true

  script:
  
    """
    iqtree \
      -s ${fasta} \
      -m GTR+I+G4 \
      -B 1000 \
      -nm 1000 \
      -T 2 \
      --seed 0 \
      --safe \
      --prefix iqtree_${fasta.getSimpleName().split('msa_')[1]}
    """
  }


process report {
  publishDir "${params.outdir}/15_report", mode: "copy", overwrite: false
  input:
    path xlsx
    
  output:
    path "*.xlsx"
    path "*.png"
  
  when:
    params.full == true

  script:
   """
    report.py -p *PRRT*.xlsx -i *INT*.xlsx -e *ENV*.xlsx
    """
}

process report_noenv {
  publishDir "${params.outdir}/15_report", mode: "copy", overwrite: false
  input:
    path xlsx
    
  output:
    path "*.xlsx"
    path "*.png"
  
  
  when:
    params.full == true

  script:
    """
    report_noenv.py -p *PRRT*.xlsx -i *INT*.xlsx
    """
}

process report_rki {
  publishDir "${params.outdir}/15_report", mode: "copy", overwrite: false
  input:
    path xlsx
    
  output:
    path "*.xlsx"
    path "*.png"
  
  when:
    params.full == true && params.rkireport == true

  script:
   """
   report.py -p *PRRT*.xlsx -i *INT*.xlsx -e *ENV*.xlsx
   """
}


process report_noenv_rki {
  publishDir "${params.outdir}/15_report", mode: "copy", overwrite: false
  input:
    path xlsx
    
  output:
    path "*.xlsx"
  
  when:
    params.full == true && params.rkireport == true

  script:
   """
    report_noenv_rki.py ${xlsx} *.xlsx
    """
}

process countplot {
  publishDir "${params.outdir}/15_report", mode: "copy", overwrite: true
  input:
    path xlsx
    
  output:
    path "*.png"
  
  when:
    params.full == true

  script:
    """
    countplot.py ${xlsx} *.png
    """
}

// Inputs
inputfasta = channel.fromPath("${projectDir}/inputs/InputFasta/*.fasta")
panelChannel = channel.fromPath("${projectDir}/inputs/References/*.fas")
graphqlChannel = channel.fromPath("${projectDir}/scripts/*.gql")
inputg2pcsv = channel.fromPath("${projectDir}/inputs/Geno2Pheno/*.csv")
inputregacsv = channel.fromPath("${projectDir}/inputs/Rega/*.csv")

workflow {
    markedfasta = mark_fasta(inputfasta)
    cometChannel = comet(markedfasta)
    input_stanfordChannel = markedfasta.filter(~/.*_PRRT_20M.fasta$|.*_INT_20M.fasta$/).combine(graphqlChannel)
    stanfordChannel = stanford(input_stanfordChannel)
    json_csvChannel = json_to_csv(stanfordChannel)  
    g2p_csvChannel = g2p(inputg2pcsv)
    rega_csvChannel = clean_rega(inputregacsv)
    int_jointChannel = join_int(json_csvChannel.filter(~/.*_INT_20M.csv$/), cometChannel.filter(~/.*_INT_20M.csv$/), g2p_csvChannel.filter(~/.*_INT_20M.csv$/), rega_csvChannel.filter(~/.*_INT_20M.csv$/))
    prrt_jointChannel = join_prrt(json_csvChannel.filter(~/.*_PRRT_20M.csv$/), cometChannel.filter(~/.*_PRRT_20M.csv$/), g2p_csvChannel.filter(~/.*_PRRT_20M.csv$/), rega_csvChannel.filter(~/.*_PRRT_20M.csv$/))

    if (params.noenv) {
      if (params.withxlsx == true) {
         inputtagxlsx = channel.fromPath("${projectDir}/AllSeqsCO20/*.xlsx")
         tag_csvChannel = get_tags(inputtagxlsx)
    } else {
         inputtagxlsx = xlsx2fragments(inputfasta.filter(~/.*_PRRT_20.fasta/), inputfasta.filter(~/.*_INT_20.fasta/))
         tag_csvChannel = get_tags(inputtagxlsx.flatten())
    }
    decision_csvChannel = make_decision_no_env(prrt_jointChannel, int_jointChannel)
    all_dfs = tag_csvChannel.concat(decision_csvChannel).collect()
    fullChannel = join_with_tags_no_env(all_dfs)
    fasta_mafftChannel = fasta_for_mafft(fullChannel.flatten())
    fullFromPathChannel = channel.fromPath("${projectDir}/${params.outdir}/10_joint_with_tags/*.xlsx").collect()
    intConcatChannel = int_concat_panel(fasta_mafftChannel.filter(~/.*_INT_.*.fasta/), panelChannel.filter(~/.*_INT_.*.fas/))
    prrtConcatChannel = prrt_concat_panel(fasta_mafftChannel.filter(~/.*_PRRT_.*.fasta/), panelChannel.filter(~/.*_PRRT_.*.fas/))
    // MAFFT
    msaChannel = mafft(prrtConcatChannel.concat(intConcatChannel))
    // IQTREE (let iqtree get modified msa files)
    mafftPathChannel = channel.fromPath("${projectDir}/${params.outdir}/13_mafft/*.fasta")
    //iqtree(msaChannel)
    iqtree(mafftPathChannel)
    
      if (params.rkireport == true) {
        //REPORT
        reportChannel = report_noenv_rki(fullFromPathChannel)
        // PLOT
        plotChannel = countplot(channel.fromPath("${projectDir}/${params.outdir}/15_report/*.xlsx"))
    } else {
        //REPORT
        reportChannel = report_noenv(fullFromPathChannel)
        // PLOT
        //plotChannel = countplot(channel.fromPath("${projectDir}/${params.outdir}/15_report/*.xlsx"))
    }
  
    } else {
        if (params.withxlsx == true) {
          inputtagxlsx = channel.fromPath("${projectDir}/AllSeqsCO20/*.xlsx")
          tag_csvChannel = get_tags(inputtagxlsx)
    } else {
          inputtagxlsx = xlsx3fragments(inputfasta.filter(~/.*_PRRT_20.fasta/), inputfasta.filter(~/.*_INT_20.fasta/), inputfasta.filter(~/.*_ENV_20.fasta/))
          tag_csvChannel = get_tags(inputtagxlsx.flatten())
    }
    env_jointChannel = join_env(cometChannel.filter(~/.*_ENV_20M.csv$/), g2p_csvChannel.filter(~/.*_ENV_20M.csv$/), rega_csvChannel.filter(~/.*_ENV_20M.csv$/))
    decision_csvChannel = make_decision(prrt_jointChannel, env_jointChannel, int_jointChannel)
    all_dfs = tag_csvChannel.concat(decision_csvChannel).collect()
    fullChannel = join_with_tags(all_dfs)
    fasta_mafftChannel = fasta_for_mafft(fullChannel.flatten())
    fullFromPathChannel = channel.fromPath("${params.outdir}/10_joint_with_tags/*.xlsx").collect()
    envConcatChannel = env_concat_panel(fasta_mafftChannel.filter(~/.*_ENV_.*.fasta/), panelChannel.filter(~/.*_ENV_.*.fas/))
    intConcatChannel = int_concat_panel(fasta_mafftChannel.filter(~/.*_INT_.*.fasta/), panelChannel.filter(~/.*_INT_.*.fas/))
    prrtConcatChannel = prrt_concat_panel(fasta_mafftChannel.filter(~/.*_PRRT_.*.fasta/), panelChannel.filter(~/.*_PRRT_.*.fas/))
    // MAFFT
    msaChannel = mafft(prrtConcatChannel.concat(intConcatChannel).concat(envConcatChannel))
    // IQTREE (let iqtree get modified msa files)
    mafftPathChannel = channel.fromPath("${projectDir}/${params.outdir}/13_mafft/*.fasta")
    iqtree(mafftPathChannel)
      if (params.rkireport == true) {
        //REPORT
        reportChannel = report_rki(fullFromPathChannel)
        // PLOT
        //plotChannel = countplot(channel.fromPath("${projectDir}/${params.outdir}/15_report/*.xlsx"))
    } else {
       //REPORT
       reportChannel = report(fullFromPathChannel)
       // PLOT
       //plotChannel = countplot(channel.fromPath("${projectDir}/${params.outdir}/15_report/*.xlsx"))
    }
  }
}

// check token