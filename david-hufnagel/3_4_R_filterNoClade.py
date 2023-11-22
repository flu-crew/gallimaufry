#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script removes all sequences in a fasta delimited by "|" that have no
clade information.
NOTE: could be used to remove "NA" field strains for anything, not just clade
Created by David E. Hufnagel on Dec 16, 2022
"""
import sys


inp = open(sys.argv[1])      #input fasta file
out = open(sys.argv[2], "w") #output filtered fasta file
col = int(sys.argv[3])-1       #the column with clade data





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





#BODY
inpDict = ReadFasta(inp)
for defline, seqs in inpDict.items():
    if len(seqs) > 1:
        print("ERROR!")
        sys.exit()
    else:
        defLst = defline.strip().split("|")
        clade = defLst[col]
        if clade not in ["","NA","unknown","Unknown"]:
            newlines = ">%s\n%s\n" % (defline, seqs[0])
            out.write(newlines)









inp.close()
out.close()