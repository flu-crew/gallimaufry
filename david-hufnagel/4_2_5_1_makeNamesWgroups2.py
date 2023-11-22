#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script takes as input names files entitled with N1 clade and generates a 
new file with defline=clade for all sequences.
Created by David E. Hufnagel on May  2, 2023

This version uses only the fasta file with clade information in that file
"""

import sys, os

#Identify input and output files
inp = open("combinedN1data_v4_clean_wClass.fna")                #Input fasta
out = open("namesWgroups.txt", "w")                             #Output groups file for MEGA using ID names
newFasta = open("combinedN1data_v4_clean_wClass_IDs.fna", "w")  #Output fasta with ID names
refTable = open("idTable.tab", "w")                             #The relationships between full deflines and ID names
cladeFiles = []





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





#Go through inp, set an ID for each defline, extract clade and output to all output files
inpDict = ReadFasta(inp)
idNum = 1
for defline, seqs in inpDict.items():
    if len(seqs) > 1:
        print("ERROR!")
        sys.exit()
    else:
        seq = seqs[0]
        defLst = defline.strip().split("|")
        clade = defLst[6].replace(".","_")
        idStr = str(idNum).zfill(6)
        
        
        #output to groups file
        newline = "%s=%s\n" % (idStr, clade)
        out.write(newline)
        
        #output to new fasta
        newlines = ">%s\n%s\n" % (idStr, seq)
        newFasta.write(newlines)
        
        #output to reference table
        newline = "%s\t%s\n" % (defline.strip(), idStr)
        refTable.write(newline)
        
        idNum += 1




inp.close()
out.close()
newFasta.close()
refTable.close()