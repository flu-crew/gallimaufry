#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 15:56:58 2021

@author: david.hufnagel
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
for defline, seq in inpDict.items():
    newDef = defline
    if len(defline.split("|")) == 6:
        newDef = "newAdditions|" + defline.strip(">")

    newlines = ">%s\n%s\n" % (newDef, seq[0])
    out.write(newlines)














inp.close()
out.close()