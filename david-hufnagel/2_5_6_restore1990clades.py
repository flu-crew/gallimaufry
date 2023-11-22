#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to restore the full clade distinction for most of
the 3.1990.4 strains
Created by David E. Hufnagel on Wed Aug 18 19:35:11 2021
"""
import sys

cladesFasta = open("mergedSeqs_v12_h3.fna")
newFasta = open("mergedSeqs_v14_h3_wE72.fna")
out = open("mergedSeqs_v14_h3_wE72_1990restore.fna", "w")
KEEPSHORT = ["A/swine/Quebec/N2020-6-4/2020", "A/England/42/72"]




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





#Go through clades fasta and make a dict of key: strain  val: fullClade
cladesFastaDict = ReadFasta(cladesFasta)
cladeDict = {}
for defline, seq in cladesFastaDict.items():
    if len(seq) == 1:  #checks for duplicate deflines
        defLst = defline.strip().split("|")
        strain = defLst[-6]; clade = defLst[-2]
        SaveIntoDict(strain, clade, cladeDict)
    else:
        print("ERROR 1!")
        sys.exit()


#Go through newFasta, and if strain is not in a small list replace the
#   partial clade with the full clade.  Output the result
newFastaDict = ReadFasta(newFasta)
for defline, seq in newFastaDict.items():
    if len(seq) == 1:
        defLst = defline.strip().split("|")
        strain = defLst[-6]
        
        if strain not in KEEPSHORT:
            newClade = cladeDict[strain][0]
            defLst[-2] = newClade
            newDef = "|".join(defLst)
        else:
            newDef = defline
            
        newlines = ">%s\n%s\n" % (newDef, seq[0])
        out.write(newlines)

    else:
        print("ERROR 2!")
        sys.exit()







cladesFasta.close()
newFasta.close()
out.close()