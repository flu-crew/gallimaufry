#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to add another empty field to strains that were brought
over from the last OFFLU report without providing a field for HI testing in 
this report 
Created by David E. Hufnagel on Jan  6, 2022
"""
import sys

inpH1 = open("mergedSeqs_h1_v11.fna")
inpH3 = open("mergedSeqs_h3_v11.fna")
outH1 = open("mergedSeqs_h1_v11_reformat.fna", "w")
outH3 = open("mergedSeqs_h3_v11_reformat.fna", "w")





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





inpH1Dict = ReadFasta(inpH1)
for defline, seq in inpH1Dict.items():
    if len(seq) > 1:
        print("ERROR1!")
        sys.exit()
    else:
        defLst = defline.strip().split("|")
        if len(defLst) == 12:
            defLst.insert(6, "")
        newDef = "|".join(defLst)
        newlines = ">%s\n%s\n" % (newDef, seq[0])
        outH1.write(newlines)


inpH3Dict = ReadFasta(inpH3)
for defline, seq in inpH3Dict.items():
    if len(seq) > 1:
        print("ERROR2!")
        sys.exit()
    else:
        defLst = defline.strip().split("|")
        if len(defLst) == 12:
            defLst.insert(6, "")
        newDef = "|".join(defLst)
        newlines = ">%s\n%s\n" % (newDef, seq[0])
        outH3.write(newlines)









inpH1.close()
inpH3.close()
outH1.close()
outH3.close()








