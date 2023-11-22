#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to label every strain that is being HI tested in this 
OFFLU report as such in the deflines
Created by David E. Hufnagel on Mon Aug 23 14:12:41 2021
"""
import sys
testStrains = open("toTest.txt")
inpH1 = open("mergedSeqs_v16_h1.fna")
inpH3 = open("mergedSeqs_v16_h3.fna")
outH1 = open("mergedSeqs_v16_h1_wTestData.fna", "w")
outH3 = open("mergedSeqs_v16_h3_wTestData.fna", "w")





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





#Go through test strains and store strain names in a list
testStrainLst = []
for line in testStrains:
    testStrainLst.append(line.strip())


#Go through inpH1 and for all strains in the list add a label that indicates
#  it is being tested in this report. Output this result
inpH1Dict = ReadFasta(inpH1)
for defline, seq in inpH1Dict.items():
    if len(seq) == 1:
        defLst = defline.strip().split("|")
        strain = defLst[-6]
        if strain in testStrainLst:
            defLst[-7] = "lab-21-b"
        newDefLst = "|".join(defLst)
        newlines = ">%s\n%s\n" % (newDefLst, seq[0])
        outH1.write(newlines)
    else:
        print("ERROR 1!")
        sys.exit()


#Go through inpH3 and for all strains in the list add a label that indicates
#  it is being tested in this report. Output this result
inpH3Dict = ReadFasta(inpH3)
for defline, seq in inpH3Dict.items():
    if len(seq) == 1:
        defLst = defline.strip().split("|")
        strain = defLst[-6]
        if strain in testStrainLst:
            defLst[-7] = "lab-21-b"
        newDefLst = "|".join(defLst)
        newlines = ">%s\n%s\n" % (newDefLst, seq[0])
        outH3.write(newlines)
    else:
        print("ERROR 2!")
        sys.exit()






testStrains.close()
inpH1.close()
inpH3.close()
outH1.close()
outH3.close()