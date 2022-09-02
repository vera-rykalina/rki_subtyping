# My Markdown Test

## Here I will try to write a simple code, using bash.

    $ nextflow ../Scripts/subtyping_pipeline.nf --outdir ../Results --run MS95
    N E X T F L O W  ~  version 22.04.4
    Launching `../Scripts/subtyping_pipeline.nf` [furious_hodgkin] DSL2 - revision: 333a2ff10d
    executor >  local (23)
    [cf/8c3339] process > mark_fasta (3)      [100%] 3 of 3 ✔
    [81/ccdddc] process > stanford (1)        [100%] 3 of 3 ✔
    [28/907f6f] process > json_to_csv (3)     [100%] 3 of 3 ✔
    [84/234416] process > rega_to_csv (1)     [100%] 3 of 3 ✔
    [6c/14640d] process > comet (2)           [100%] 3 of 3 ✔
    [14/7da948] process > prrt_joint (1)      [100%] 1 of 1 ✔
    [cf/83225a] process > env_joint (1)       [100%] 1 of 1 ✔  
    [2f/847e9f] process > int_joint (1)       [100%] 1 of 1 ✔
    [15/761046] process > tags_to_csv (3)     [100%] 3 of 3 ✔
    [66/8de6bb] process > decision_to_csv (1) [100%] 1 of 1 ✔
    [b5/161910] process > full_joint          [100%] 1 of 1 ✔
    [-        ] process > report              -
    [-        ] process > phylo_fasta         -
    Completed at: 16-Aug-2022 23:23:46
    Duration    : 4m 16s
    CPU hours   : 0.4
    Succeeded   : 23


>Why not to try a code block?

```sh {bash ls}
ls .
```