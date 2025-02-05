#!/usr/bin/env python3

"""clean_gtf.py: Takes a gtf file from agat_convert_sp_gff2gtf.pl
to add extra required fields in the 9th column containing key,
value keys for metadata.Here is more information about required field:
https://www.sudosight.com/RNA-seek/RNA-seq/build/#3-hybrid-genomes

It is recommended running this program with a version of python greater
than '3.8'. This ensures that the order of the key,value pairs in the
9th column is retained.

# Steps for converting messy gff into properly formatted GTF file
# 1. Pull image from registry and create SIF
module load singularity 
SINGULARITY_CACHEDIR=$PWD singularity pull \\
    docker://quay.io/biocontainers/agat:0.8.0--pl5262hdfd78af_0 

# 2. Run AGAT todo the heavy lifting of gtf conversion
singularity exec -B $PWD \\
    agat_0.8.0--pl5262hdfd78af_0.sif agat_convert_sp_gff2gtf.pl \\
        --gff /path/to/input.gff \\
        -o /path/to/converted.gtf

# 3. Finally run this script
module load python/3.9
./clean_gtf.py /path/to/converted.gtf > /path/to/clean.gtf
"""

# Python standard library
from __future__ import print_function
import sys, re


def stripped(v):
    """Cleans string to remove quotes"""
    return v.strip('"').strip("'")


def lookup(mykey, dictionary):
    """ Tries to lookup value in dictionary using an 
    exact match if the key. Returns empty string if 
    not found. """
    v = ''
    if mykey in dictionary:
        v = dictionary[mykey]
        v = stripped(v)
    return v


def contains(pattern, dictionary):
    """Flexible lookup that searches for a pattern
    instead of a key. Returns empty string if pattern
    is not found in dictionary.
    """
    v = ''
    kys = dictionary.keys()
    for k in kys:
        if pattern in k:
            v = dictionary[k]
            break
    return v


def parse(linelist):
    """Parses key, value pairs in 9th column and returns
    and index (dictionary) of all fields.
    """
    tags = {}  # store key, value pairs in 9th column 
    metadata = re.split('; ', linelist[8].rstrip(';'))
    for field in metadata: 
        k,v = field.split(' ', 1)
        tags[k] = v.strip('"').strip("'")
    return tags


def default(v, d):
    """Returns d when v is empty (string, list, etc) or false"""
    if not v:
        v = d    
    return v


def biotypes(gtf):
    """Creates dictionary to map each gene to its biotype.
    biotype features listed as mRNA will be converted to 
    protein_coding.
    """
    gene2type = {}
    with open(sys.argv[1]) as file:
        for line in file:
            if line.startswith('#'):
                # Skip over comments in header section
                continue
            linelist = line.strip().split('\t')
            metadata = parse(linelist)
            # Get gene and biotype 
            gene = lookup('gene_id', metadata)
            # Setting biotype to unknown as default
            # value, then checking if metadata contains
            # any fields with biotype as a sub string, 
            # then if biotype is not an empty string 
            # set it to whatever is in the gtf file
            if gene not in gene2type:
                gene2type[gene] = "unknown"
            biotype = contains('biotype', metadata)
            if default(biotype, 'unknown') != 'unknown':
                if biotype.lower() == 'mrna':
                    # agat_convert_sp_gff2gtf.pl does 
                    # not set this value correct even 
                    # when it is in the original GTF 
                    # file, fixing the problem for 
                    # RSeQC TIN reference file
                    biotype = 'protein_coding'
                gene2type[gene] = biotype

    return gene2type


def formatted(metadata):
    """Reformats key, value metadata to be written into the
    9th column.
    """
    out = ''
    for k,v in metadata.items():
        out += '{} "{}"; '.format(k,v)
    out = out.rstrip(' ')
    return out

def main():
    if len(sys.argv) != 2:
        print('Usage: python {} genes.gtf > protein_coding_genes.lst'.format(sys.argv[0]))
        print('\nError: failed to provide all positional arguments!', file=sys.stderr)
        sys.exit(1)

    input_gtf = sys.argv[1]
    g2b = biotypes(input_gtf)

    with open(input_gtf) as file:
        for line in file:
            if line.startswith('#'):
                # Skip over comments in header section
                print(line.strip())
                continue
            linelist = line.strip().split('\t')
            feature = linelist[2]
            metadata = parse(linelist)
            # Should always be in GTF file
            gene_id = lookup('gene_id', metadata)
            if feature == 'gene':
                # May not be in GTF, add as needed
                gene_name = default(lookup('gene_name', metadata) , gene_id)
                metadata['gene_name'] = gene_name
                gene_biotype = default(lookup('gene_biotype', metadata) , g2b[gene_id])
                metadata['gene_biotype'] = gene_biotype
            elif feature in ['transcript', 'exon']:
                # May not be in GTF, add as needed
                # assumes transcript_id is in gtf
                gene_name = default(lookup('gene_name', metadata) , gene_id)
                metadata['gene_name'] = gene_name
                gene_biotype = default(lookup('gene_biotype', metadata) , g2b[gene_id])
                metadata['gene_biotype'] = gene_biotype
                transcript_id = lookup('transcript_id', metadata)
                transcript_name = default(lookup('transcript_name', metadata) , transcript_id)
                metadata['transcript_name'] = transcript_name
                transcript_type = default(lookup('transcript_type', metadata) , g2b[gene_id])
                metadata['transcript_type'] = transcript_type
            tags = formatted(metadata)
            linelist[8] = tags
            print("\t".join(linelist))


if __name__ == '__main__':
    main()

