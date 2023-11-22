#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take an OFFLU fasta file and split it into
separate files by clade with a filter for the number of sequences per clade.
It also keeps only sequences with the provenances publicIAV and offluVCM.
Created by David E. Hufnagel on Mon Aug 23 15:46:25 2021
"""
import sys

inp = open(sys.argv[1])
minCladeSize = int(sys.argv[2])





def SaveIntoDict(key, val, dictx):
    if key in dictx:
        dictx[key].append(val)
    else:
        dictx[key] = [val,]

def ReadFasta(fd): #Go through inp and store the file in a dict of key: defline   val: seq
    fastaDict = {}
    oldDef = ""; oldSeq = ""
    for line in fd:
        if line.startswith(">"):
            if oldSeq != "":
                SaveIntoDict(oldDef, oldSeq, fastaDict)
                oldDef = line.strip().strip(">")
                oldSeq = ""
            else:
                oldDef = line.strip().strip(">")
        else:
            oldSeq += line.strip()
    else:
        SaveIntoDict(oldDef, oldSeq, fastaDict)
        
    return(fastaDict)





#Go through the input file, filter by provenance, and make a dict of 
#   key: clade  val: [(deflineA, seqA), (deflineB, seqB)...]
inpDict = ReadFasta(inp)
cladeDict = {}
for defline, seq in inpDict.items():
    if len(seq) > 1:
        print("ERROR!")
        sys.exit()
    else:
        defLst = defline.strip().split("|")
        prov = defLst[0]
        clade = defLst[-2]
        if prov in ["offlu-vcm", "publicIAV"] and "onsensus" not in defline:
            pair = (defline, seq[0])
            SaveIntoDict(clade, pair, cladeDict)


#Go through the dict, filter by clade size, and output all remaining data
for clade, data in cladeDict.items():
    fileName = "%s.fna" % (clade)
    if len(data) >= minCladeSize:
        out = open(fileName, "w")
        for pair in data:
            newlines = ">%s\n%s\n" % (pair[0], pair[1])
            out.write(newlines)
            
        out.close()





inp.close()