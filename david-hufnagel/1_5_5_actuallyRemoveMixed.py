#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Upon finding that a fasta file where mixed strains were supposed to be removed
contained mixed strains I wrote this script to remove them once and for all.

Created by David E. Hufnagel on Wed Feb  3, 2021
"""
import sys

inp = open(sys.argv[1])      #allN1s_v3_aligned_reformat_noMixed.fna
out = open(sys.argv[2], "w") #allN1s_v3_aligned_reformat_trueNoMixed.fna



for line in inp:
    if line.startswith(">"):
        lineLst = line.strip().split("|")
        clade = lineLst[5]
        if "__" in clade:
            toKeep = False
        else:
            toKeep = True
            out.write(line)
    else:
        if toKeep:
            out.write(line)




inp.close()
out.close()