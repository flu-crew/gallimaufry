#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to add CVVs, variants, and vaccines from the previous
reports to my current OFFLU data files
Created by David E. Hufnagel on Jan  4, 2022
"""
import sys


oldH1 = open("mergedSeqs_v19_h1.fna")
oldH3 = open("mergedSeqs_v17_h3.fna")
newH1 = open("mergedSeqs_h1_v8.fna")
newH3 = open("mergedSeqs_h3_v7_noDups_cladeFix.fna")
outH1 = open("mergedSeqs_h1_v9.fna", "w")
outH3 = open("mergedSeqs_h3_v9.fna", "w")





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





#Go through new fastas and output everything
for line in newH1.readlines():
    outH1.write(line)
    
for line in newH3.readlines():
    outH3.write(line)


#Go through old fastas and output CVVs, variants, vaccines, and reference strains
oldH1Dict = ReadFasta(oldH1)
for defline, seq in oldH1Dict.items():
    if len(seq) > 1:
        print("ERROR1!")
        sys.exit()
    else:
        if "onsensus" not in defline:
            defLst = defline.strip().split("|")
            prov = defLst[0]
            if prov in ["CVV", "SwReference", "huReference", "huVaccine", "variant"]:
                if len(defLst) == 7:
                    for i in range(6):
                        defLst.insert(1, "")
                newDef = "|".join(defLst)
                newlines = ">%s\n%s\n" % (newDef, seq[0])
                outH1.write(newlines)
                
                
#Go through old fastas and output CVVs, variants, vaccines, and reference strains
oldH3Dict = ReadFasta(oldH3)
for defline, seq in oldH3Dict.items():
    if len(seq) > 1:
        print("ERROR2!")
        sys.exit()
    else:
        if "onsensus" not in defline:
            defLst = defline.strip().split("|")
            prov = defLst[0]
            if prov in ["CVV", "SwReference", "huReference", "huVaccine", "variant"]:
                if len(defLst) == 7:
                    for i in range(6):
                        defLst.insert(1, "")
                newDef = "|".join(defLst)
                newlines = ">%s\n%s\n" % (newDef, seq[0])
                outH3.write(newlines)














oldH1.close()
oldH3.close()
newH1.close()
newH3.close()
outH1.close()
outH3.close()











