#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to remove strain duplicates from any fasta file with 
| delimited deflines
Created by David E. Hufnagel on Mon May  9, 2022
"""
import sys
inp = open(sys.argv[1])           #fasta input
outFasta = open(sys.argv[2], "w") #main fasta output
outDups = open(sys.argv[3], "w")  #duplicates output
strainLoc = int(sys.argv[4])-1    #the index (starting with 1) of the strain name





def SaveIntoDict(key, val, dictx):
    if key in dictx:
        dictx[key].append(val)
    else:
        dictx[key] = [val,]


def ReadFasta(fd): #Go through input and store the file in a dict of key: strain   val: seq as well as a dict of key: strain  val: defline
    seqDict = {}; defDict = {}
    oldDef = ""; oldSeq = ""
    for line in fd:
        if line.startswith(">"):
            if oldSeq != "":
                oldStrain = oldDef.split("|")[strainLoc]
                SaveIntoDict(oldStrain, oldSeq, seqDict)
                SaveIntoDict(oldStrain, oldDef, defDict)
                oldDef = line.strip().strip(">")
                oldSeq = ""
            else:
                oldDef = line.strip().strip(">")
        else:
            oldSeq += line.strip()
    else:
        oldStrain = oldDef.split("|")[strainLoc]
        SaveIntoDict(oldStrain, oldSeq, seqDict)
        SaveIntoDict(oldStrain, oldDef, defDict)
    return(seqDict, defDict)





#strains involved in defline duplicates are output to a duplicates file, 
#   and the rest is output to the main fasta file
seqDict, defDict = ReadFasta(inp)
idNum = 1
for strain, seq in seqDict.items():
    defline = defDict[strain]
    if len(seq) == 1:
        newlines = ">%s\n%s\n" % (defline[0], seq[0])
        outFasta.write(newlines)      
    else:
        for i in range(len(seq)):
            newlines = ">%s__%s\n%s\n" % (defline[i], idNum, seq[i])
            outDups.write(newlines)  
            idNum += 1








inp.close()
outFasta.close()
outDups.close()