#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take a large fasta and annotate strains designated
for HI testing.

Created by David E. Hufnagel on Aug 26, 2020
"""
import sys


fasta = open(sys.argv[1])
hisFd = open(sys.argv[2])
out = open(sys.argv[3], "w")



#Go through hisFd and make a list of strains to label
his = []
for line in hisFd:
    his.append(line.strip().split("\t")[1])
    

#Go through fasta and mark HI strains, creating a new output
for line in fasta:
    if line.startswith(">"):
        lineLst = line.strip().strip(">").split("|")
        strain = lineLst[1]
        if strain in his:
            newSource = "forHI"
            end = "|".join(lineLst[1:])
            newDef = ">%s|%s\n" % (newSource, end)
            out.write(newDef)
        else:
            out.write(line)
    else:
        out.write(line)




fasta.close()
hisFd.close()
out.close()