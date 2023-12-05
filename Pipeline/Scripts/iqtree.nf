nextflow.enable.dsl = 2

projectDir = "/scratch/rykalinav/rki_subtyping/Pipeline"

params.outdir = null
if (!params.outdir) {
  println "outdir: $params.outdir"
  error "Missing output directory!"
}

fastaChannel = channel.fromPath("${projectDir}/InputFasta/*.fasta")
panelChannel = channel.fromPath("${projectDir}/References/*.fas")

workflow {
    // CAT
    envConcatChannel = env_concat_panel(fastaChannel.filter(~/.*_ENV_.*.fasta/), panelChannel.filter(~/.*_ENV_.*.fas/))
    intConcatChannel = int_concat_panel(fastaChannel.filter(~/.*_INT_.*.fasta/), panelChannel.filter(~/.*_INT_.*.fas/))
    prrtConcatChannel = prrt_concat_panel(fastaChannel.filter(~/.*_PRRT_.*.fasta/), panelChannel.filter(~/.*_PRRT_.*.fas/))
    // MAFFT
    msaChannel = mafft(prrtConcatChannel.concat(intConcatChannel).concat(envConcatChannel))
    // IQTREE
    iqtree(msaChannel)
 }

process prrt_concat_panel {
  publishDir "${params.outdir}/1_concat_with_panel", mode: "copy", overwrite: true
  
  input:
    path fragment
    path ref

  output:
    path "concat_${fragment.getSimpleName()}.fasta"

  script:
    """
    cat ${fragment} ${ref} > concat_${fragment.getSimpleName()}.fasta 
    """ 
    
  } 

process int_concat_panel {
  publishDir "${params.outdir}/1_concat_with_panel", mode: "copy", overwrite: true
  input:
    path fragment
    path ref

  output:
      path "concat_${fragment.getSimpleName()}.fasta"

  script:
    """
    cat ${fragment} ${ref} > concat_${fragment.getSimpleName()}.fasta 
    """ 
    
  } 

process env_concat_panel {
  publishDir "${params.outdir}/1_concat_with_panel", mode: "copy", overwrite: true
  input:
    path fragment
    path ref

  output:
    path "concat_${fragment.getSimpleName()}.fasta"

  script:
    """
    cat ${fragment} ${ref} > concat_${fragment.getSimpleName()}.fasta 
    """  
  } 


process mafft {
  publishDir "${params.outdir}/2_mafft", mode: "copy", overwrite: true
  input:
      path fasta
  output:
      path  "msa_${fasta.getSimpleName().split('concat_')[1]}.fasta"

  script:
  
    """
    mafft --auto ${fasta} > msa_${fasta.getSimpleName().split('concat_')[1]}.fasta
    """
  }

process iqtree {
  label "iqtree"
  publishDir "${params.outdir}/3_iqtree", mode: "copy", overwrite: true
  input:
      path fasta
  output:
      path  "*.treefile"
      path  "*.iqtree"
      path  "*.log"

  script:
  
    """
    iqtree \
      -s ${fasta} \
      -m GTR+I+G4 \
      -B 10000 \
      -nm 10000 \
      -T ${task.cpus} \
      --prefix iqtree_${fasta.getSimpleName().split('msa_')[1]} 
    """
  }

/*
 What is suggested:
 iqtree -s ${fasta} -pre iqtree_${fasta.getSimpleName().split('msa_')[1]} -m GTR+I+G4 -bb 10000 -nt 4 -nm 10000
 Suggestions from Vera:
 -T AUTO instead of -nt 4 to check the threads  (the best is 2 cores)
 --seed 0 (good for publications)
 --bnni (Optimize UFBoot trees by NNI on bootstrap alignment)
 --safe (Turn on safe numerical mode to avoid numerical underflow for large data sets with 
 many sequences (typically in the order of thousands). 
 This mode is automatically turned on when having more than 2000 sequences.)

 Discuss 
 http://www.iqtree.org/doc/Tutorial#reducing-impact-of-severe-model-violations-with-ufboot
 -B (--ufboot -bb - previeios version)
 -n 10000 (norammlly set to 0)
 -n 0 (Skip subsequent tree search, useful when you only want to assess the phylogenetic information of the alignment.)
*/