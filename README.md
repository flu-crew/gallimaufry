# gallimaufry
A collection of useful scripts

## Requirements

The scripts in this repo should run on any UNIX system (Linux or MacOS).

The scripts in this repo use the following command line tools:

 * `mafft` - a popular sequence alignment tool
 * `smof` - a sequence manipulation utility available on PyPi


## Extract HA1 regions

The scripts `extractHA1.sh` and `extractHA1-CDS.sh` extract the HA1 amino acid
or coding sequence, respectively, from an HA gene. Currently it these scripts
will work automatically for H1 or H3 segments.

The regions are extracted by first aligning the input DNA sequence and then
finding the locations of each HA1 match on the gapped sequences. The interval
that is most common is used to take substrings from the aligned sequences. This
approach is very robust against bad or unusual sequences. It will work so long
as more sequences match the given pattern then match any other irregular
pattern.

For H1, the expected HA1 regular expression pattern is `DT[LI]C.*QSR`. For H3,
it is `QKL.*QTR`.

For an input file `myseq.fasta`, the files `myseq.fasta.aln` (the multiple
sequence alignment) and `myseq.fasta_HA1.faa` (for `extactHA1.sh`) or
`myseq.fasta_HA1.fna` (for `extractHA1-CDS.sh`) will be created.

## Extract H1 Antigenic sites
The script 'antigenic_motif.py' extracts the antigenic sites from aligned H1 nucleotide data. 
It will convert the nucleotide data into amino acid sequence and will extract the relevant sites.
Sites are extracted based on H1 numbering.
List of sites:
'''Ca-1	169	173	207					
Ca-2	140	143	145	224	225			
Cb	78	79	80	81	82	83	122	
Sa	128	129	158	160	162	163	165	167
Sb	156	159	192	193	196	198	

For input file, align your H1 nucleotide data.
Run it as, python antigenic_motif.py aligned_input.fasta'''

Output will be written to aligned_input.fasta-AB-AntigenicSites.txt
