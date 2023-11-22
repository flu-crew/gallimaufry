#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script takes as input names files entitled with N1 clade and an alignment 
fasta file and generates a new fasta file with clade information in the
appropriate column for all sequences.
Created by David E. Hufnagel on May  2, 2023
"""

import sys, os

#Identify input and output files
inp = open("combinedN1data_v4_clean.fna")
out = open("combinedN1data_v4_clean_wClass.fna", "w")
cladeFiles = []
for file in os.listdir():
    if "names" in file:
        cladeFiles.append(file)





#Define functions
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

def ConvertClade(oldClade): #Converts a clade ID to a nice looking clade label
    newClade = "N1"
    for i in range(2,len(oldClade)):
        newClade += "."
        newClade += oldClade[i]
    return(newClade)





#Go through names files and make a dict of key: defline name: clade
cladeDict = {}
for file in cladeFiles:
    fd = open(file)
    clade = ConvertClade(file.split("_")[0])
    for line in fd:
        cladeDict[line.strip().replace("(","_").replace(")","_").replace("'","_").replace("|","_").replace("-","_").replace("/","_").strip("_")] = clade
    fd.close()


#Go through the fasta, match deflines to clades, and output the resulting
#   fasta data with clade information
inpDict = ReadFasta(inp)
for defline, seqs in inpDict.items():
    if len(seqs) > 1:
        print("ERROR!")
        sys.exit()
    else:
        seq = seqs[0]
        if "REF" not in defline:
            defLst = defline.strip().split("|")
            clade = cladeDict[defline.strip().replace("(","_").replace(")","_").replace("'","_").replace("|","_").replace("-","_").replace("/","_").strip("NEW_").strip("_")]
            defLst[6] = clade
            newDef = "|".join(defLst)
            newlines = ">%s\n%s\n" % (newDef, seq)
        else:
            newlines = ">%s\n%s\n" % (defline, seq)
        out.write(newlines)






inp.close()
out.close()