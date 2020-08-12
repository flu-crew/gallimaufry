#!/usr/bin/env bash

set -u
set -e

seq=$1

A="(GCA|GCC|GCG|GCT)"
C="(TGC|TGT)"
D="(GAC|GAT)"
E="(GAA|GAG)"
F="(TTC|TTT)"
G="(GGA|GGC|GGG|GGT)"
H="(CAC|CAT)"
I="(ATA|ATC|ATT)"
K="(AAA|AAG)"
L="(CTA|CTC|CTG|CTT|TTA|TTG)"
M="(ATG)"
N="(AAC|AAT)"
P="(CCA|CCC|CCG|CCT)"
Q="(CAA|CAG)"
R="(AGA|AGG|CGA|CGC|CGG|CGT)"
S="(AGC|AGT|TCA|TCC|TCG|TCT)"
T="(ACA|ACC|ACG|ACT)"
V="(GTA|GTC|GTG|GTT)"
W="(TGG)"
Y="(TAC|TAT)"
X="(...)"

# A regular expression that should capture the entire HA1 region
H1_HA_regex="$D$T($L|$I)$C$X*$Q$S$R"
H3_HA_regex="$Q$K$L$X*$Q$T$R"

mafft $seq > $seq.aln 2> /dev/null

# get the bounds for the H1 region
bounds=$(smof grep -qP --gff  "$H1_HA_regex|$H3_HA_regex" $seq.aln | cut -f4,5 | sort | uniq -c | sort -rg | head -1 | sed 's/ *[0-9]* *//')

smof subseq -b $bounds $seq.aln | smof clean -u > ${seq}_HA1.fna

echo ">> Input sequence summary:"
smof stat $seq
echo

echo ">> Filtered sequence summary (after removing sequences with less than 1500 nn)"
smof filter -l $MIN_LENGTH $seq | smof stat
echo

echo ">> Selected bounds for the HA1 region from the protein alignment: $bounds"
echo

echo  ">> Summary of HA regions"
smof stat ${seq}_HA1.fna

echo " * This number should match the number of filtered sequences, if not you either have bad sequence or need to change the regex"
echo

echo ">> Detailed summary of HA1 output:"
smof sniff ${seq}_HA1.fna
echo " * All sequences should be proteins and there should be no internal stops"
