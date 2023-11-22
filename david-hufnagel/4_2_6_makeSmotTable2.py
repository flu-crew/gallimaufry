#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is takes a "|" delimited fasta file and makes a table smot can 
use to classify in the following format:
defline     clade
Created on Thu Sep 28 10:28:39 2023
This version is strain only
"""
import sys


inp = open(sys.argv[1])
out = open(sys.argv[2], "w")
cladeInd = int(sys.argv[3])-1 #index of clade information starting with 1
strainInd = int(sys.argv[4])-1 #index of strain information starting with 1



for line in inp:
    if line.startswith(">"):
        defline = line.strip().strip(">")
        lineLst = defline.split("|")
        clade = lineLst[cladeInd]
        strain = lineLst[strainInd]
        newline = "%s\t%s\n" % (strain, clade)   
        out.write(newline)




inp.close()
out.close()