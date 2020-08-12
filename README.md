# gallimaufry
A collection of useful scripts


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
