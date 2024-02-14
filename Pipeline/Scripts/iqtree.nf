nextflow.enable.dsl = 2

//projectDir = "/scratch/rykalinav/rki_subtyping/Pipeline"
projectDir = params.projectdir

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
      -B 5000 \
      -nm 5000 \
      -T 2 \
      -cptime 3600 \
      --prefix iqtree_${fasta.getSimpleName().split('msa_')[1]} 
    """
  }
