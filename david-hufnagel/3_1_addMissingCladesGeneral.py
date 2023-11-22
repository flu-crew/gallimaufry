#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to use octoFLU classifier data to add clade info
to an OFFLU fasta where it is missing.

Created by David E. Hufnagel on Dec 28, 2021
"""
import sys

inp = open(sys.argv[1])      #input fasta file
classFD = open(sys.argv[2])  #input octoFLU classifier file
out = open(sys.argv[3], "w") #output fasta with clade information
cladeCol = int(sys.argv[4])  #the python index of the clade in inp (consider underscores in strain names)




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





#Go through classFD and make a dict of key: defline val: clade
cladeDict = {}
for line in classFD:
    lineLst = line.strip().split("\t")
    defline = lineLst[0]
    clade = lineLst[-2]
    cladeDict[defline] = clade    
    
#Go through inp, fill in missing clade info, and pipe to output splitting
#   H1 and H3
inpDict = ReadFasta(inp)
for defline, seq in inpDict.items():
    if len(seq) > 1:
        print("ERROR!")
        sys.exit()
    else:
        defLst = defline.split("|")
        clade = cladeDict[defline]
        if clade not in ["ND","NA","unknown"]:
            defLst[cladeCol] = clade

        newdef = "|".join(defLst)
        newlines = ">%s\n%s\n" % (newdef, seq[0])     
        out.write(newlines)







inp.close()
classFD.close()
out.close()








