#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take a file containing clade information and a big
fasta file and split that file up by clade into smaller fasta files.  Also
makes a full sized fasta file with clade information added before country.

Created by David E. Hufnagel on Jul 29, 2020
"""
import sys

fasta = open(sys.argv[1])
cladesFd = open(sys.argv[2])
bigOut = open(sys.argv[3], "w")



def SaveIntoDict(key, val, dictx):
    if key in dictx:
        dictx[key].append(val)
    else:
        dictx[key] = [val,]



#Go through clades file and make a dict of key: defline  val: clade
cladeDict = {}
cladesFd.readline()
for line in cladesFd:
    lineLst = line.strip().split("\t")
    defline = lineLst[0]
    clade = lineLst[1]
    cladeDict[defline] = clade


#Go through the fasta file and save deflines and seqs into a dict of key:
#  clade  val: [(defline,seq),(defline,seq),...]
fastaDict = {}  #dict of key: defline  val: seq
lastDef = ""
lastSeq = ""
for line in fasta:
    if line.startswith(">"):
        defline = line.strip().strip(">")
        if lastDef != "":
            clade = cladeDict[lastDef]
            SaveIntoDict(clade, (lastDef,lastSeq), fastaDict)
            lastSeq = ""
        lastDef = defline
    else:
        lastSeq += line.strip()
else:
    clade = cladeDict[lastDef]
    SaveIntoDict(clade, (lastDef,lastSeq), fastaDict)
        

#Go through the fasta dict and write to outputs
for clade, pairs in fastaDict.items():
    cladeOutName = "%sOnly.fna" % (clade)
    cladeOut = open(cladeOutName, "w")
    
    for pair in pairs:   
        #Write to big fasta output
        defline = pair[0]
        before = "|".join(defline.strip().split("|")[:4])
        after = "|".join(defline.strip().split("|")[4:])
        seq = pair[1]
        newline = ">%s|%s|%s\n%s\n" % (before, clade, after, seq)
        bigOut.write(newline)
        
        #Write to clade-specific fasta outputs
        cladeOut.write(newline)
        
    cladeOut.close()
        
        








fasta.close()
cladesFd.close()
bigOut.close()
