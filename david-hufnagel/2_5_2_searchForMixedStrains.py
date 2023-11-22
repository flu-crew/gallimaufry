#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to look for and, if necessary, strip an OFFLU fasta
file of mixed strains
Created by David E. Hufnagel on Wed Jul 14 21:29:44 2021
"""
import sys

inp = open(sys.argv[1])





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
        subtype = defline.split("|")[-5]
        print(subtype)
    else:
        print("ERROR!")
        sys.exit()





inp.close()
