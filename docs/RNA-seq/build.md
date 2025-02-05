# <code>rna-seek <b>build</b></code>

## 1. About 
The `rna-seek` executable is composed of several inter-related sub commands. Please see `rna-seek -h` for all available options.

This part of the documentation describes options and concepts for <code>rna-seek <b>build</b></code> sub command in more detail. With minimal configuration, the **`build`** sub command enables you to build new reference files for the RNA-seek run pipeline.    

Setting up the RNA-seek build pipeline is fast and easy! In its most basic form, <code>rna-seek <b>build</b></code> only has *five required inputs*.

## 2. Synopsis
```text
$ ./rna-seek build [-h] --ref-fa REF_FA
                        --ref-name REF_NAME
                        --ref-gtf REF_GTF
                        --gtf-ver GTF_VER
                        --output OUTPUT
                        [--dry-run]
                        [--singularity-cache SINGULARITY_CACHE]
                        [--sif-cache SIF_CACHE]
```

The synopsis for each command shows its parameters and their usage. Optional parameters are shown in square brackets.

A user **must** provide the genomic sequence of the reference's assembly in FASTA format via `--ref-fa` argument, an alias for the reference genome via `--ref-name` argument, a gene annotation for the reference assembly via `--ref-gtf` argument, an alias or version for the gene annotation via the ` --gtf-ver` argument, and an output directory to store the built reference files via `--output` argument.

For [human](https://www.gencodegenes.org/human/) and [mouse](https://www.gencodegenes.org/mouse/) data, we highly recommend downloading the latest available `PRI` genome assembly and corresponding gene annotation from [GENCODE](https://www.gencodegenes.org/). These reference files contain chromosomes and scaffolds sequences. 

 The build pipeline will generate a JSON file containing key, value pairs to required reference files for the <code>rna-seek <b>run</b></code> pipeline. This file will be located in the path provided to `--output`. The name of this JSON file is dependent on the values provided to `--ref-name` and `--gtf-ver` and has the following naming convention: `{OUTPUT}/{REF_NAME}_{GTF_VER}.json`. Once the build pipeline completes, this reference JSON file can be passed to the `--genome` option of <code>rna-seek <b>run</b></code>. This is how new references are built for the RNA-seek pipeline. 

Use you can always use the `-h` option for information on a specific command. 

### 2.1 Required Arguments

Each of the following arguments are required. Failure to provide a required argument will result in a non-zero exit-code.

  `--ref-fa REF_FA`  
> **Genomic FASTA file of the reference genome.**  
> *type: string*
> 
> This file represents the genome sequence of the reference assembly in FASTA format. If you are downloading this from GENCODE, you should select the *PRI* genomic FASTA file. This file will contain the primary genomic assembly (contains chromosomes and scaffolds). This input file should not be compressed. Sequence identifers in this file must match with sequence identifers in the GTF file provided to `--ref-gtf`.  
> 
> ***Example:***
> `--ref-fa GRCh38.primary_assembly.genome.fa`


---  
  `--ref-name REF_NAME`  
> **Name of the reference genome.**  
> *type: string*
> 
> Name or alias for the reference genome. This can be the common name for the reference genome. Here is a list of common examples for different model organisms: mm10, hg38, rn6, danRer11, dm6, canFam3, sacCer3, ce11. If the provided values contains one of the following sub-strings (hg19, hs37d, grch37, hg38, hs38d, grch38, mm10, grcm38), then Arriba will run with its corresponding blacklist. 
> 
> ***Example:*** `--ref-name hg38`

--- 
  `--ref-gtf REF_GTF`  
> **Gene annotation or GTF file for the reference genome.**  
> *type: string*
> 
> This file represents the reference genome's gene annotation in GTF format. If you are downloading this from GENCODE, you should select the 'PRI' GTF file. This file contains gene annotations for the primary assembly (contains chromosomes and scaffolds). This input file should not be compressed. Sequence identifers (column 1) in this file must match with sequence identifers in the FASTA file provided to `--ref-fa`.  
> ***Example:***  `--ref-gtf gencode.v36.primary_assembly.annotation.gtf`

---
  `--gtf-ver GTF_VER`  
> **Version of the gene annotation or GTF file provided.**  
> *type: string or int*
> 
> This is the version of the supplied gene annotation or GTF file. If you are using a GTF file from GENCODE, use the release number or version (i.e. *M25* for mouse or *37* for human). Visit gencodegenes.org for more details.  
> ***Example:*** `--gtf-ver 36`
  
--- 
  `--output OUTPUT`
> **Version of the gene annotation or GTF file provided.**  
> *type: string or int*
>   
> This location is where the build pipeline will create all of its output files. If the user-provided working directory has not been initialized, it will automatically be created.  
> ***Example:*** `--output /scratch/$USER/refs/hg38_v36/`

### 2.2 Options

Each of the following arguments are optional and do not need to be provided. 

  `-h, --help`            
> **Display Help.**  
> *type: boolean*
> 
> Shows command's synopsis, help message, and an example command
> 
> ***Example:*** `--help`

---  
  `--dry-run`            
> **Dry run the build pipeline.**  
> *type: boolean*
> 
> Displays what steps in the build pipeline remain or will be run. Does not execute anything!
>
> ***Example:*** `--dry-run`

--- 
  `--singularity-cache SINGULARITY_CACHE`  
> **Overrides the $SINGULARITY_CACHEDIR environment variable.**  
> *type: string*  
> *default: `--output OUTPUT/.singularity`*
>
> Singularity will cache image layers pulled from remote registries. This ultimately speeds up the process of pull an image from DockerHub if an image layer already exists in the singularity cache directory. By default, the cache is set to the value provided to the `--output` argument. Please note that this cache cannot be shared across users. Singularity strictly enforces you own the cache directory and will return a non-zero exit code if you do not own the cache directory! See the `--sif-cache` option to create a shareable resource. 
> 
> ***Example:*** `--singularity-cache /data/$USER/.singularity`

---  
  `--sif-cache SIF_CACHE`
> **Path where a local cache of SIFs are stored.**  
> *type: string*  
>
> Uses a local cache of SIFs on the filesystem. This SIF cache can be shared across users if permissions are set correctly. If a SIF does not exist in the SIF cache, the image will be pulled from Dockerhub and a warning message will be displayed. The `rna-seek cache` subcommand can be used to create a local SIF cache. Please see `rna-seek cache` for more information. This command is extremely useful for avoiding DockerHub pull rate limits. It also remove any potential errors that could occur due to network issues or DockerHub being temporarily unavailable. We recommend running RNA-seek with this option when ever possible.
> 
> ***Example:*** `--singularity-cache /data/$USER/SIFs`
> 


## 3. Hybrid Genomes  

If you have two GTF files, e.g. hybrid genomes (host + virus), then you need to create one genomic FASTA file and one GTF file for the hybrid genome prior to running the <code>rna-seek <b>build</b></code> command. 

We recommend creating an artifical chromosome for the non-host sequence. The sequence identifer in the FASTA file must match the sequence identifer in the GTF file (column 1). Generally speaking, since the host annotation is usually downloaded from Ensembl or GENCODE, it will be correctly formatted; however, that may not be the case for the non-host sequence!

Please ensure the non-host annotation contains the following features and/or constraints:   

 * for a given `gene` feature   
     * each `gene` entry has at least one `transcript` feature    
     * and each `transcript` entry has atleast one `exon` feature 

If not, the GTF file may need to be manually curated until these conditions are satisfied. 

Here is an example feature from a hand-curated Biotyn_probe GTF file:

```bash
Biot1   BiotynProbe gene    1   21  0.000000    +   .   gene_id "Biot1"; gene_name "Biot1"; gene_biotype "biotynlated_probe_control";
Biot1   BiotynProbe transcript  1   21  0.000000    +   .   gene_id "Biot1"; gene_name "Biot1"; gene_biotype "biotynlated_probe_control"; transcript_id "Biot1"; transcript_name "Biot1"; transcript_type "biotynlated_probe_control";
Biot1   BiotynProbe exon    1   21  0.000000    +   .   gene_id "Biot1"; gene_biotype "biotynlated_probe_control"; transcript_id "Biot1"; transcript_type "biotynlated_probe_control";
```

In this tab-delimited example above, 

 * ***line 1:*** the `gene` feature has 3 required attributes in column 9: `gene_id` and `gene_name` and `gene_biotype`
 * ***line 2:*** the `transcript` entry for the above `gene` repeats the same attributes with following required fields: `transcript_id ` and `transcript_name`
     * *Please note:* `transcript_type` is *optional*
 * ***line 3:*** the `exon` entry for the above `transcript` has 3 required attributes: `gene_id` and `transcript_id` and `gene_biotype`
     * *Please note:* `transcript_type` is *optional*

For a given gene, the combination of the `gene_id` AND `gene_name` should form a unique string. There should be no instances where two different genes share the same `gene_id` AND `gene_name`. 


## 4. Convert NCBI GFF3 to GTF format

It is worth noting that RNA-seek comes bundled with a script to convert GFF3 files downloaded from NCBI to GTF file format. This convenience script is useful as the `rna-seek build` sub command takes a GTF file as one of its inputs. 

Please note that this script has only been tested with GFF3 files downloaded from NCBI, and _it is **not** recommended to use with GFF3 files originating from other sources like Ensembl or GENCODE_. If you are selecting an annotation from Ensembl or GENCODE, please download the GTF file option.

The only dependecy of the script is the python package argparse, which comes bundled with the following python2/3 distributions: `python>=2.7.18` or `python>=3.2`. If argparse is not installed, it can be downloaded with pip by running the following command:

```bash
pip install argparse
```

For more information about the script and its usage, please run:
```bash
./resources/gff3togtf.py -h
```

## 5. Example
```bash 
# Step 0.) Grab an interactive node (do not run on head node)
srun -N 1 -n 1 --time=12:00:00 -p interactive --mem=8gb  --cpus-per-task=4 --pty bash
module purge
module load singularity snakemake

# Step 1.) Dry run the Build pipeline
./rna-seek build --ref-fa GRCm39.primary_assembly.genome.fa \
                 --ref-name mm39 \
                 --ref-gtf gencode.vM26.annotation.gtf \
                 --gtf-ver M26 \
                 --output /scratch/$USER/refs/mm39_M26 \
                 --dry-run

# Step 2.) Build new RNA-seek reference files 
./rna-seek build --ref-fa GRCm39.primary_assembly.genome.fa \
                 --ref-name mm39 \
                 --ref-gtf gencode.vM26.annotation.gtf \
                 --gtf-ver M26 \
                 --output /scratch/$USER/refs/mm39_M26
```
