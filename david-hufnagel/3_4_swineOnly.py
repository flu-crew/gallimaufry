#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take a fasta file with a "|" delimiter as input 
and output only sequences with a swine origin
Created by David E. Hufnagel on Oct 17, 2022
"""
import sys
inp = open(sys.argv[1])      #input fasta
out = open(sys.argv[2], "w") #output swine-only fasta
col = int(sys.argv[3])-1     #column where the host information is stored starting with 1
delim = "|"                  #delimiter





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
    defLst = defline.split(delim)
    host = defLst[col]
    
    if host in ["Swine","swine","SWINE","pig","Pig","PIG","boar","Boar","BOAR"]:
        if len(seqs) == 1:
            seq = seqs[0]
            newlines = ">%s\n%s\n" % (defline, seq)
            out.write(newlines)
        else:
            for seq in seqs:
                newlines = ">%s\n%s\n" % (defline, seq)
                out.write(newlines)










inp.close()
out.close()