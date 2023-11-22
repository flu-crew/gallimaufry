#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take a "|" delimited fasta file, replace the "/"s
with "-"s


Created by David E. Hufnagel on Dec 2, 2021
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
    if len(seq) != 1:
        print("ERROR!")
        sys.exit()
    else:
        defLst = defline.split("|")
        date = defLst[-1].replace("/","_")
        defLst[-1] = date
        newDef = "|".join(defLst)
        newlines = ">%s\n%s\n" % (newDef, seq[0])
        out.write(newlines)






inp.close()
out.close() 
