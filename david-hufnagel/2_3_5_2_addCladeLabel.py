#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to add gamma clade information to each sequence in
a fasta file using names extracted.
Created by David E. Hufnagel on Thu Jun 17 16:16:55 2021
"""
import sys

fasta = open("allGammas_v3_ORFtrim_min4_clean.fna")
c1Names = open("C1names.txt")
c2Names = open("C2names.txt")
c3Names = open("C3names.txt")
preNames = open("preSplitnames.txt")
unNames = open("unAssignednames.txt")
out = open("allGammas_v3_ORFtrim_min4_clean_wGclades.fna", "w")





def ProcessNamesFile(fd):
    names = []
    for line in fd:
        names.append(line.strip())
        
    return(names)


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





#Go through each names file and store names in lists
c1NamesLst = ProcessNamesFile(c1Names)
c2NamesLst = ProcessNamesFile(c2Names)
c3NamesLst = ProcessNamesFile(c3Names)
preNamesLst = ProcessNamesFile(preNames)
unNamesLst = ProcessNamesFile(unNames)


#Go through fasta, add gamma clade info, and output the data
fastaDict = ReadFasta(fasta)
for defline, seq in fastaDict.items():
    if len(seq) == 1:
        defLst = defline.strip().strip(">").split("|")
        clade = defLst[5]
        if defline.strip() in c1NamesLst:
            clade += "_C1"
        elif defline.strip() in c2NamesLst:
            clade += "_C2"
        elif defline.strip() in c3NamesLst:
            clade += "_C3"
        elif defline.strip() in preNamesLst:
            clade += "_pre"
        elif defline.strip() in unNamesLst:
            clade += "_un"
        else:
            print("ERROR1!")
            sys.exit()
    else:
        print("ERROR2!")
        sys.exit()
        
        
    defLst[5] = clade
    newDef = "|".join(defLst)
    newlines = ">%s\n%s\n" % (newDef, seq[0])
    out.write(newlines)












fasta
c1Names
c2Names
c3Names
preNames
unNames
out