#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take a fasta file downloaded from IRD, and make a
new fasta with only HA sequences. Also seperates defline duplicates into
their own file.

Created by David E. Hufnagel on May  6, 2022
"""
import sys

inp = open("hAandNAall.fasta")
out = open("haAll.fasta", "w")
outDups = open("dups.fasta", "w")





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





#Go through inp, output most lines, and make a list for duplicate deflines of
#   tuples of (defline, newlines)
cnt = 1
inpDict = ReadFasta(inp)
dupDefs = [] #a list of tuples of (defline, newlines)
for defline, seq in inpDict.items():
    seg = int(defline.split("|")[2])
    if seg == 4: #keep only HA sequences
        if len(seq) != 1:
            for x in seq:
                newlines = ">%s__%s\n%s\n" % (defline, cnt, x)
                newTup = (defline, newlines)        
                dupDefs.append(newTup)
                cnt += 1
            
        else:
            seg = int(defline.split("|")[2])
            if seg == 4:
                newlines = ">%s\n%s\n" % (defline, seq[0])
                out.write(newlines)


#Sort duplicate list and output duplicate lines
for tup in dupDefs:
    outDups.write(tup[1])





inp.close()
out.close() 
outDups.close()