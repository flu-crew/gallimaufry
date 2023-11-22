#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script cuts out amino acid sequences that don't start with 'M' or that
have multiple stop codons
Created by David E. Hufnagel on Jun  3, 2023
"""
import sys

inp = open(sys.argv[1])
out = open(sys.argv[2], "w")





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
for defline, seqs in inpDict.items():
    if len(seqs) > 1:
        print("ERROR!")
        sys.exit()
    else:
        seq = seqs[0]
        defLst = defline.strip().split("|")
        if seq.count("*") <= 1 and seq.startswith("M"):
            newlines = ">%s\n%s\n" % (defline, seq)
            out.write(newlines)




inp.close()
out.close()