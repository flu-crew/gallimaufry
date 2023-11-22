#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 10:38:13 2023

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





#BODY
inpDict = ReadFasta(inp)
for defline, seqs in inpDict.items():
    if len(seqs) > 1:
        print("ERROR!")
        sys.exit()
    else:
        seq = seqs[0]
        defLst = defline.split("|")
        if len(defLst) == 1: #barcode line
            newlines = ">%s|\n%s\n" % (defline, seq)
        else:
            newlines = ">%s|%s\n%s\n" % (defLst[0], defLst[5], seq)
        out.write(newlines)







inp.close()
out.close()