#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to reformat and normalize Canadian fasta data
Created by David E. Hufnagel on Sun Dec 20, 2020
"""
import sys

fasta = open(sys.argv[1])      #input fasta (the seqs octoFLU didn't exclude)
extra = open(sys.argv[2])      #input fasta (the seqs octoFLU did exclude)
out = open(sys.argv[3], "w")   #output fasta file



#Go through inp, reformat, and output for fasta
for line in fasta:
    if line.startswith(">"):
        lineLst = line.strip().strip(">").split("|")
        strain = lineLst[0]
        date = lineLst[-1]; year = date.split("-")[0]
        subtype = lineLst[1]
        newStrain = "A/swine/%s/%s" % ("_".join(strain.split("_")[2:]).replace("_","-"), year)
        newline = ">offlu-vcm|%s|%s|swine|CAN||%s\n" % (newStrain, subtype, date)
        out.write(newline)
    else:
        out.write(line)


#Go through inp, reformat, and output for extra
for line in extra:
    if line.startswith(">"):
        lineLst = line.strip().strip(">").split(" ")
        strain = lineLst[0]; subtype = "-".join(lineLst[1:])
        newline = ">offlu-vcm|%s|%s|swine|CAN||\n" % (strain, subtype)
        out.write(newline)
    else:
        if line.strip() != "":
            out.write(line)



fasta.close()
extra.close()
out.close()