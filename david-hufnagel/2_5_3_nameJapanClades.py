#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take the 1A OFFLU fasta file and add clade 
information for japanese strains
Created by David E. Hufnagel on Tue Jul 20 13:23:02 2021
"""
import sys
inp = open("mergedSeqs_v9_h1_1A.fna")
cladeData = open("tentative-clade-names.txt")
out = open("mergedSeqs_v9_h1_1A_wJPNclades.fna", "w")





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





#Go through cladeData and make a dict of key: strain  val: clade
cladeDict = {}
for line in cladeData:
    defLst = line.strip().split("|")
    strain = defLst[-6]
    clade = defLst[-2]
    SaveIntoDict(strain, clade, cladeDict)


#Go through inp, add clade information where available, and output the result
inpDict = ReadFasta(inp)
for defline, seq in inpDict.items():
    if len(seq) == 1:
        defLst = defline.split("|")
        oldClade = defLst[-2]
        strain = defLst[-6]
        
        if strain in cladeDict:
            newClade = cladeDict[strain][0]
            defLst[-2] = newClade
            newDef = "|".join(defLst)
            newlines = ">%s\n%s\n" % (newDef, seq[0])
        else:
            newlines = ">%s\n%s\n" % (defline, seq[0])
        out.write(newlines)
    else:
        print("ERROR!")
        sys.exit()
    
    











inp.close()
cladeData.close()
out.close()