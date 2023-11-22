#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to add chosen duplicate strains back into the main
fasta file.
Created by David E. Hufnagel on Wed Jun  2, 2021
"""

fasta = open("allGammas_v2_noDups.fna")
dups = open("dups_sort.fna")
out = open("allGammas_v3.fna", "w")
CHOSEN = [1,3,6,8,10,11,14,16,18,21,23,24,26,28,32,34,36,38,40,42,46,48,49,51,54,55,58,60,62,63,66,67,70,71,75]




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





#Read the fasta file and write it directly to the output
for line in fasta:
    out.write(line)

#Go through dups, choose the right sequences based on CHOSEN and output them
dupDict = ReadFasta(dups)
for defline, seq in dupDict.items():
    ID = int(defline.split("_")[-1])
    newDef = "_".join(defline.split("_")[:-1]) 

    if len(seq) != 1:
        print("ERROR!")

    if ID in CHOSEN:
        newline = ">%s\n%s\n" % (newDef, seq[0])
        out.write(newline)







fasta.close()
dups.close()
out.close()