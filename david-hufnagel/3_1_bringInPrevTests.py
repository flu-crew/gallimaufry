#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take the current versions of our OFFLU fasta files
and add in previously tested strains from the last report. As part of this
integration the deflines are reformatting to include lab testing information
including an empty field for the current report.

Created by David E. Hufnagel on Jan  3, 2022
"""
import sys

newH1 = open("mergedSeqs_h1_v6.fna")
newH3 = open("mergedSeqs_h3_v6.fna")
oldH1 = open("PrevReportsData/mergedSeqs_v19_h1.fna")
oldH3 = open("PrevReportsData/mergedSeqs_v17_h3.fna")
outH1 = open("mergedSeqs_h1_v7.fna", "w")
outH3 = open("mergedSeqs_h3_v7.fna", "w")





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





#Go through oldH1, output previously tested strains and make a list of strains
#  output
oldH1Dict = ReadFasta(oldH1)
addedStrains = []
for defline, seq in oldH1Dict.items():
    if len(seq) > 1:
        print("ERROR1!")
        sys.exit()
    else:
        if not defline.startswith("Consensus"):
            defLst = defline.split("|")
            defLst.insert(6,"") #add blank spot for 2022 lab test
            strain = defLst[7]
            addedStrains.append(strain)
            
            allTests = "".join(defLst[1:7])
            if allTests != "" and defLst[0] in ["offlu-vcm", "publicIAV"]:
                newlines = ">%s\n%s\n" % ("|".join(defLst), seq[0])
                outH1.write(newlines)


#Go through oldH3, output previously tested strains and make a list of strains
#  output
oldH3Dict = ReadFasta(oldH3)
for defline, seq in oldH3Dict.items():
    if len(seq) > 1:
        print("ERROR2!")
        sys.exit()
    else:
        if not defline.startswith("Consensus"):
            defLst = defline.split("|")
            defLst.insert(6,"") #add blank spot for 2022 lab test
            strain = defLst[7]
            addedStrains.append(strain)
            
            allTests = "".join(defLst[1:7])
            if allTests != "" and defLst[0] in ["offlu-vcm", "publicIAV"]:
                newlines = ">%s\n%s\n" % ("|".join(defLst), seq[0])
                outH3.write(newlines)


#Go through newH1, reformat, and output where the strain was not already output
#  from the last report
newH1Dict = ReadFasta(newH1)
for defline, seq in newH1Dict.items():
    if len(seq) > 1:
        print("ERROR3!")
        sys.exit()
    else:
        if not defline.startswith("Consensus"):
            defLst = defline.split("|")
            strain = defLst[1]
            if not strain in addedStrains:
                for x in range(6):
                    defLst.insert(1,"")
                    
                newlines = ">%s\n%s\n" % ("|".join(defLst), seq[0])
                outH1.write(newlines)
        else:
            newlines = ">%s\n%s\n" % (defline, seq[0])
            outH1.write(newlines)


#Go through newH3, reformat, and output where the strain was not already output
#  from the last report
newH3Dict = ReadFasta(newH3)
for defline, seq in newH3Dict.items():
    if len(seq) > 1:
        print("ERROR4!")
        sys.exit()
    else:
        if not defline.startswith("Consensus"):
            defLst = defline.split("|")
            strain = defLst[1]
            if not strain in addedStrains:
                for x in range(6):
                    defLst.insert(1,"")
                    
                newlines = ">%s\n%s\n" % ("|".join(defLst), seq[0])
                outH3.write(newlines)
        else:
            newlines = ">%s\n%s\n" % (defline, seq[0])
            outH3.write(newlines)









newH1.close()
newH3.close()
oldH1.close()
oldH3.close()
outH1.close()
outH3.close()













