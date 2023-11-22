#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to add gamma clade information to each sequence in
a fasta file using names extracted.
Created by David E. Hufnagel on Thu Jun 17 16:16:55 2021
Updated on June 21st, 2021 to add clade identifiers specifically for clades 
C3.1 and C3.2
"""
import sys

fasta = open("allGammas_v3_ORFtrim_min4_clean_wGclades_wCons2.aln")
c3_1Names = open("C1.1names.txt")
c3_2Names = open("C1.2names.txt")
out = open("allGammas_v3_ORFtrim_min4_clean_wGclades_wCons2_C3names.aln", "w")





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
c3_1NamesLst = ProcessNamesFile(c3_1Names)
c3_2NamesLst = ProcessNamesFile(c3_2Names)


#Go through fasta, add gamma clade info, and output the data
fastaDict = ReadFasta(fasta)
for defline, seq in fastaDict.items():
    if len(seq) == 1:
        if not "onsensus" in defline:
            defLst = defline.strip().strip(">").split("|")
            clade = defLst[5]
            if defline.strip() in c3_1NamesLst:
                clade += ".1"
            elif defline.strip() in c3_2NamesLst:
                clade += ".2"
                
            defLst[5] = clade
            newDef = "|".join(defLst)
            newlines = ">%s\n%s\n" % (newDef, seq[0])
        else:
            newlines = ">%s\n%s\n" % (defline, seq[0])
            
        
    else:
        print("ERROR2!")
        sys.exit()
        
    out.write(newlines)
        
        










fasta.close()
c3_1Names.close()
c3_2Names.close()
out.close()