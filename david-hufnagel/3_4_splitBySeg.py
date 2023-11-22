#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to split a fasta by gene segment
Created by David E. Hufnagel on Tue Sep 27 09:39:38 2022
"""
import sys
inp = open(sys.argv[1])    #input fasta file
segInd = int(sys.argv[2]) #index of segment identifier





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





inpDict = ReadFasta(inp)
for defline, seq in inpDict.items():
    if len(seq) == 1:
        pass
    else:
        pass






inp.close()