#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to reformat and normalize French fasta data
Created by David E. Hufnagel on Mon Dec 21, 2020
"""
import sys


fasta = open(sys.argv[1])    #input fasta
meta = open(sys.argv[2])     #input metadata file
out = open(sys.argv[3], "w") #output fasta





def CreateSubtype(start):
    sub = "%s%s" % (start[:2],start[-2:])
    
    return(sub)





#Go through metadata and make a dict of key: strain  val: date
metaDict = {}
meta.readline()
for line in meta:
    lineLst = line.strip().split("\t")
    strain = lineLst[0].split(" ")[0]
    metaDict[strain] = lineLst[4]


#Go through fasta, collect subtype and date information, format and output
toKeep = False
for line in fasta:
    if line.startswith(">"):
        if line.startswith(">HA"):
            toKeep = True
            lineLst = line.strip().split("|")
            strain = lineLst[2]
            subtype = CreateSubtype(lineLst[3])
            date = metaDict[strain]

            newline = ">offlu-vcm|%s|%s|swine|FRA||%s\n" % (strain, subtype, date)
            out.write(newline)
        else:
            toKeep = False
    else:
        if toKeep == True:
            out.write(line)




fasta.close()       
meta.close()    
out.close()
