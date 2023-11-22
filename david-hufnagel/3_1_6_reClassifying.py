#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to reclassify all OFFLU sequences based on Tavis'
recommendations

Created by David E. Hufnagel on Jan  4, 2022
"""
import sys

inpH1 = open("mergedSeqs_h1_v9.fna")
inpH3 = open("mergedSeqs_h3_v9.fna")
classH1 = open("classifications.output.H1")
classH3 = open("classifications.output.H3")
outH1 = open("mergedSeqs_h1_v9_reclassed.fna", "w")
outH3 = open("mergedSeqs_h3_v9_reclassed.fna", "w")





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





#Go through H1 classification and make a dict of key: strain  val: clade
classH1Dict = {}
classH1.readline()
for line in classH1.readlines():
    if "onsensus" not in line:
        lineLst = line.strip().split("\t")
        strain = lineLst[0].split("|")[1]
        clade = lineLst[1]
        classH1Dict[strain] = clade
   

#Go through H3 classification and make a dict of key: strain  val: clade
classH3Dict = {}
classH3.readline()
for line in classH3.readlines():
    if "onsensus" not in line:
        lineLst = line.strip().split("\t")
        strain = lineLst[0].split("|")[1]
        clade = lineLst[1]
        classH3Dict[strain] = clade


#Go through inpH1, reclassify, and output 
h1Dict = ReadFasta(inpH1)
for defline, seq in h1Dict.items():
    if len(seq) > 1:
        print("ERROR1!")
        sys.exit()
    else:
        if "onsensus" in defline:
            newlines = ">%s\n%s\n" % (defline, seq[0])
            outH1.write(newlines)
        else:
            defLst = defline.strip().split("|")
            clade = defLst[-2]
            strain = defLst[-6]
            if strain in classH1Dict:
                newClade = classH1Dict[strain]
            else:
                newClade = clade
            
            defLst[-2] = newClade
            newDef = "|".join(defLst)
            newlines = ">%s\n%s\n" % (newDef, seq[0])
            outH1.write(newlines)
            
            # if strain == "A/swine/Denmark/2015_04775_1p1/2015":
            #     print(clade)
            #     print(newDef)
            # sys.exit()
            

#Go through inpH3, reclassify, and output 
h3Dict = ReadFasta(inpH3)
for defline, seq in h3Dict.items():
    if len(seq) > 1:
        print("ERROR2!")
        sys.exit()
    else:
        if "onsensus" in defline:
            newlines = ">%s\n%s\n" % (defline, seq[0])
            outH3.write(newlines)
        else:
            defLst = defline.strip().split("|")
            clade = defLst[-2]
            strain = defLst[-6]
            if strain in classH3Dict:
                newClade = classH3Dict[strain]
            else:
                newClade = clade
            
            defLst[-2] = newClade
            newDef = "|".join(defLst)
            newlines = ">%s\n%s\n" % (newDef, seq[0])
            outH3.write(newlines)












inpH1.close()
inpH3.close()
classH1.close()
classH3.close()
outH1.close()
outH3.close()












