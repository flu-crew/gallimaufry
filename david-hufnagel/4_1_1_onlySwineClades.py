#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script overwrites the clade position in every defline in all but swine
strains
Created  by David E. Hufnagel one Mar 14, 2023
"""
import sys

inp = open(sys.argv[1])          #input fasta
out = open(sys.argv[2], "w")     #output fasta
hostLoc = int(sys.argv[3]) - 1   #field with host information in the defline starting with 1
cladeLoc = int(sys.argv[4]) - 1  #field with clade information in the defline starting with 1





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
        defLst = defline.strip().split("|")
        host = defLst[hostLoc]; clade = defLst[cladeLoc]

        if host not in ("Swine", "swine"):
            defLst[cladeLoc] = "NA"
            
        newDef = "|".join(defLst)
        newlines = ">%s\n%s\n" % (newDef, seq)
        out.write(newlines)




inp.close()
out.close()