#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created by David E. Hufnagel on Mon Jun 14 16:10:53 2021
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
    if len(seq) != 1:
        print(defline)
        
        
        
        
inp.close()