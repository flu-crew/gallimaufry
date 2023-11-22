#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to filter by and add information about clades to our
1A distance fasta file.
Created by David E. Hufnagel on Mon Apr 12 16:41:46 2021
"""
import sys


fasta = open(sys.argv[1])    #forDistanceSeqs_all.fna
irdFd = open(sys.argv[2])    #swineH1CladeAssignment.txt
out = open(sys.argv[3], "w")



#Go through octoFd and make a dict of key: defline  val: (subtype, clade)
cladeDict = {}
for line in irdFd:
    lineLst = line.strip().split("\t")
    defline = lineLst[0]
    clade = lineLst[2]
    if clade.startswith("1A"):
        subtype = "H1"
        cladeDict[defline] = (subtype, clade)


#Go through fasta and output all 1A seqs with deflines thath include subtype and clade
toKeepLast = False; lastDef = ""; lastSeq = ""
for line in fasta:
    if line.startswith(">"):
        defline = line.strip().strip(">")
        if toKeepLast == True:
            subtype = cladeDict[lastDef][0]
            clade = cladeDict[lastDef][1]
            
            newDefLst = lastDef.split("|")
            newDefLst[1] = subtype; newDefLst[4] = clade
            newDef = ">%s\n" % ("|".join(newDefLst))
            lastSeq = "%s\n" % (lastSeq)
            
            out.write(newDef.replace(" ", "_"))
            out.write(lastSeq)
            
            lastDef = ""; lastSeq = ""
            
        if defline in cladeDict:
            toKeepLast = True
            lastDef = defline
        else:
            toKeepLast = False
    else:
        if toKeepLast == True:
            lastSeq += line.strip()
else:
    subtype = cladeDict[lastDef][0]
    clade = cladeDict[lastDef][1]
    
    newDefLst = lastDef.split("|")
    newDefLst[1] = subtype; newDefLst[4] = clade
    newDef = ">%s\n" % ("|".join(newDefLst))
    lastSeq = "%s\n" % (lastSeq)
    
    out.write(newDef.replace(" ", "_"))
    out.write(lastSeq)    








fasta.close()
irdFd.close()
out.close()