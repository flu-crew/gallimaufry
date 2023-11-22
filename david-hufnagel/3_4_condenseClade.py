#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script takes a fasta file with clade information in a certain column
and condenses it. Specifically the following conversions are done:
1990.4.X --> 1990.4, 3.1990.4 --> 1990.4, 3.1990.4.4 --> 1990.4

Created by David E. Hufnagel on Dec 28, 2022
"""
import sys

inp = open(sys.argv[1])       #input fasta file
out = open(sys.argv[2], "w")  #output fasta file with condensed clades
cladeCol = int(sys.argv[3])-1 #column of clade info starting with 1





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
for defline,seqs in inpDict.items():
    if len(seqs) > 1:
        print("ERROR!")
        sys.exit()
    else:
        seq = seqs[0]
        lineLst = defline.strip().split("|")
        clade = lineLst[cladeCol]
        if clade in ["1990.4.a","1990.4.b1","1990.4.b2","1990.4.c","1990.4.d",\
                     "1990.4.e","1990.4.f","1990.4.g","1990.4.h","1990.4.i",\
                         "1990.4.j","1990.4.k","3.1990.4","3.1990.4.4"]:
            clade = "1990.4"
        lineLst[cladeCol] = clade
        newDef = "|".join(lineLst)
        newlines = ">%s\n%s\n" % (newDef,seq)
        out.write(newlines)
        
        
        
        
        
        
        
inp.close()
out.close()








