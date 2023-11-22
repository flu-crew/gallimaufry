#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script takes an input fasta file and retains only N1 strains
Created by David E. Hufnagel on Thu Sep 28, 2023
"""
import sys

inp = open("reference-v4.fasta")
out = open("reference-v4_N1.fasta", "w")






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





#Go through input fasta, capture N1 sequences and output them
inpDict = ReadFasta(inp)
for defline, seqs in inpDict.items():
    if len(seqs) > 1:
        print("ERROR!")
        sys.exit()
    else:
        seq = seqs[0]
        defLst = defline.strip().split("|")
        if len(defLst) == 7:
            pass #they were all N2s
        if len(defLst) == 8:
            seg = defLst[-3]
            if seg == "N1":
                defLst[-3] = ""
                newDef = "|".join(defLst)
                newlines = ">TEST|%s\n%s\n" % (newDef, seq)
                out.write(newlines)
                
    














inp.close()
out.close()








