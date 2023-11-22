#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created by David E. Hufnagel on Thu May  6 14:26:55 2021
"""
import sys

fasta = open(sys.argv[1])
replaceFD = open(sys.argv[2])
out = open(sys.argv[3], "w")



#Go through replace file and make a dict of key: defline val: clade
replaceDict = {}
for line in replaceFD:
    lineLst = line.strip().split("\t")    
    if "CY041849" in line:
        replaceDict[lineLst[0]] = "2002"
    else:
        replaceDict[lineLst[0]] = lineLst[1]


#Go through fasta and replace the first field with the clade using the dict
for line in fasta:
    if line.startswith(">"):
        
        defLst = line.strip().split("|")
        if line.strip().strip(">") in replaceDict:
            defLst[0] = replaceDict[line.strip().strip(">")]
        newline = "|".join(defLst) + "\n"
        out.write(newline)

    else:
        out.write(line)








fasta.close()
replaceFD.close()
out.close()