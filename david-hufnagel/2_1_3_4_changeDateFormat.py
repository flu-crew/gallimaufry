#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take the tabular input metadata file and modify the
dates so that they're more standard.  Also fixes every clade being associated
with the gamma clade
Created by David E. Hufnagel on Thu Sep  2 17:12:04 2021
"""

import sys
inp = open("strainMetaData_v2.txt")
out = open("strainMetaData_v3.txt", "w")
cladeFasta = open("allN1s_v4.fna")



#Go through the fasta file and make a dict of key: strain  val: HAclade
cladeDict = {}
for line in cladeFasta:
    if line.startswith(">"):
        lineLst = line.strip().split("|")
        strain = lineLst[1]
        haClade = lineLst[-2]
        cladeDict[strain] = haClade


#Go through old metadata file, fix the date, and output the result
out.write(inp.readline())
for line in inp:
    lineLst = line.strip().split("\t")
    date = lineLst[2].split("/")
    if len(date) == 3:
        newDate = "%s-%s-%s" % (date[2], date[0], date[1])
    elif len(date) == 2:
        newDate = "%s-%s" % (date[1], date[0])
    elif len(date) == 1:
        newDate = date[0]
    else:
        print("ERROR!")
        sys.exit()
        
    lineLst[2] = newDate
    lineLst[-5] = cladeDict[lineLst[0]]
    newline = "\t".join(lineLst) + "\n"
    out.write(newline)
    
    

    
    
    
    
    
inp.close()
out.close()
cladeFasta.close()