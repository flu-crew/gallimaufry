#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script removes mixed subtype infections from an IAV fasta file and
outputs subtypes present
Created by David E. Hufnagel on Thu Sep 29 16:09:46 2022
"""
import sys
inp = open(sys.argv[1])
out = open(sys.argv[2], "w")





#Define functions
def SaveIntoDict(key, val, dictx):
    if key in dictx:
        dictx[key].append(val)
    else:
        dictx[key] = [val,]

        
def ReadFasta(fd): #Go through input and store the file in a dict of key: defline   val: seq
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





#Go through input, output non-mixed samples and build a list of remaining subtypes
inpDict = ReadFasta(inp)
subs = set([])
for defline, seq in inpDict.items():
    if len(seq) == 1:
        defLst = defline.split("|")
        sub = defLst[2]
        if not "ixed" in sub:
            subs.add(sub)
            newlines = ">%s\n%s\n" % (defline, seq[0])
            out.write(newlines)
    else:
        print("ERROR!")
        sys.exit()
        
        
#Go through the list of subtypes and output them to the stdout
print("Remaining subtypes:")
for sub in subs:
    print(sub)
        





inp.close()
out.close()