#!/usr/bin/env bash

set -u
set -e

seq=$1

# A regular expression that should capture the entire HA1 region
H1_HA_regex="DT[LI]C.*QSR"
H3_HA_regex="QKL.*QTR"
MIN_LENGTH=1500

# make an alignment of all sequences longer than 1500
smof filter -l $MIN_LENGTH $seq | smof translate -f | mafft /dev/stdin > $seq.aln 2> /dev/null

# get the bounds for the H1 region
bounds=$(smof grep -qP --gff  "$H1_HA_regex|$H3_HA_regex" $seq.aln | cut -f4,5 | sort | uniq -c | sort -rg | head -1 | sed 's/ *[0-9]* *//')

smof subseq -b $bounds $seq.aln | smof clean -u > ${seq}_HA1.faa

echo ">> Input sequence summary:"
smof stat $seq
echo

echo ">> Filtered sequence summary (after removing sequences with less than 1500 nn)"
smof filter -l $MIN_LENGTH $seq | smof stat
echo

echo ">> Selected bounds for the HA1 region from the protein alignment: $bounds"
echo

echo  ">> Summary of HA regions"
smof stat ${seq}_HA1.faa

echo " * This number should match the number of filtered sequences, if not you either have bad sequence or need to change the regex"
echo

echo ">> Detailed summary of HA1 output:"
smof sniff ${seq}_HA1.faa
echo " * All sequences should be proteins and there should be no internal stops"
