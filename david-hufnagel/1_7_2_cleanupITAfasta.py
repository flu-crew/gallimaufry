#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to reformat and normalize Italian fasta data
Created by David E. Hufnagel on Mon Dec 21 09:47:01 2020
"""
import sys


fasta = open(sys.argv[1])    #input fasta
meta = open(sys.argv[2])     #input metadata file
out = open(sys.argv[3], "w") #output fasta



#Go through metadata and make a dict of key: strain  val: (subtype, date)
metaDict = {}
meta.readline()
for line in meta:
    lineLst = line.strip().split("\t")
    metaDict[lineLst[0]] = (lineLst[3], lineLst[4])


#Go through fasta, collect subtype and date information, format and output
for line in fasta:
    if line.startswith(">"):
        strain = line.strip().strip(">")
        simpleStrain = strain.replace("/","_")
        subtype = metaDict[simpleStrain][0]
        date = metaDict[simpleStrain][1]
        newline = ">offlu-vcm|%s|%s|swine|ITA||%s\n" % (strain, subtype, date)
        out.write(newline)
    else:
        out.write(line)




fasta.close()       
meta.close()    
out.close()
