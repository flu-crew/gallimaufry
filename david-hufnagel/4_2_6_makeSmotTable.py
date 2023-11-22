#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is takes a "|" delimited fasta file and makes a table smot can 
use to classify in the following format:
defline     clade
Created on Thu Sep 28 10:28:39 2023
"""
import sys


inp = open(sys.argv[1])
out = open(sys.argv[2], "w")
cladeInd = int(sys.argv[3])-1 #index of clade information starting with 1




for line in inp:
    if line.startswith(">"):
        defline = line.strip().strip(">")
        lineLst = defline.split("|")
        clade = lineLst[cladeInd]
        newline = "%s\t%s\n" % (defline, clade)   
        out.write(newline)




inp.close()
out.close()