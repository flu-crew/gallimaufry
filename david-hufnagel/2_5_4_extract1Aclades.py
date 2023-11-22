#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take a specific fasta file and extract all members
of the clades 1A.1.1, 1A.2, 1A.3.3.2, and 1A.3.3.3 into smaller fasta files
Created by David E. Hufnagel on Thu Jul 22 11:38:21 2021
"""
import sys
inp = open("mergedSeqs_v10_h1_1A.fna")
out11 = open("seqsWprevTest_1A.1.1.fna", "w")
out2 = open("seqsWprevTest_1A.2.fna", "w")
out332 = open("seqsWprevTest_1A.3.3.2.fna", "w")
out333 = open("seqsWprevTest_1A.3.3.3.fna", "w")





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





#Go through the inp, determine clades, and output accordingly
inpDict = ReadFasta(inp)
for defline, seq in inpDict.items():
    if len(seq) == 1:
        newlines = ">%s\n%s\n" % (defline, seq[0])
        
        clade = defline.split("|")[-2]
        if clade == "1A.1.1":
            out11.write(newlines)
        elif clade == "1A.2":
            out2.write(newlines)
        elif clade == "1A.3.3.2":
            out332.write(newlines)
        elif clade == "1A.3.3.3":
            out333.write(newlines)
    else:
        print("ERROR!")
        sys.exit()













inp.close()
out11.close()
out2.close()
out332.close()
out333.close()