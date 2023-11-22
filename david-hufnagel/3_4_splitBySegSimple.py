#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Split the fasta file by segment
Created by David E. Hufnagel on Tue Sep 27 10:31:21 2022
"""
import sys
inp = open(sys.argv[1])
indSeg = int(sys.argv[2])-1 #Index of the segment identifier starting with one





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





inpDict = ReadFasta(inp)
seenSegs = []         #A list of segments that have been seen before
outDict = {}          #A dict of output files containing key: seg val: associated output file
for defline, seq in inpDict.items():
    newlines = ">%s\n%s\n" % (defline, seq[0])
    if len(seq) == 1:        #Simple no duplicate case
        defLst = defline.strip().split("|")
        seg = defLst[indSeg]
        oldName = str(sys.argv[1])
        oldRoot = ".".join(oldName.split(".")[:-1])
        newName = "%s_seg%s.fasta" % (oldRoot, seg)
        if not seg in seenSegs:
            seenSegs.append(seg)
            out = open(newName, "w")
            outDict[seg] = out
            
            
        outDict[seg].write(newlines)
    elif len(seq) >= 2:
        print("ERROR!")
        sys.exit()






inp.close()