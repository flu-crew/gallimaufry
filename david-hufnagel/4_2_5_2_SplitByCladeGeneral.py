#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script takes a fasta file and breaks it into smaller fastas by clade
Created by David E. Hufnagel on May  9, 2023
"""
import sys

#Prompt user
inp = open(sys.argv[1])       #input fasta file
cladeInd = int(sys.argv[2])-1 #index of clade starting with 1





#Define classes
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





###   BODY   ###
#Go through input fasta dict, split it by clade and create a dict of 
#  key: clade  val: [newlinesA, newlinesB,...]
cladeDict = {}
inpDict = ReadFasta(inp)
for defline, seqs in inpDict.items():
    if len(seqs) > 1:
        print("ERROR!")
        sys.exit()
    else:
        seq = seqs[0]
        defLst = defline.strip().split("|")
        clade = defLst[cladeInd]
        
        newlines = ">%s\n%s\n" % (defline, seq)
        SaveIntoDict(clade, newlines, cladeDict)


#Go through the clade dict, name and open output fastas for writing, and 
#  write to the output
for clade, newlinesClade in cladeDict.items():
    outFileName = "only_%s.fna" % (clade)
    outFd = open(outFileName, "w")
    for newlines in newlinesClade:
        outFd.write(newlines)
    outFd.close()
    






#close files
inp.close()