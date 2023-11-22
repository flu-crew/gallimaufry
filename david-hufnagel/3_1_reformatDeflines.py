#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take advantage of all information in the deflines
of private sequences from the UK as well as fix their strain names. Also, this
script enforces the naming scheme "A/swine" at the start of the strain names
for all private data
Created by David E. Hufnagel on Dec 30, 2021
"""
import sys

inpH1 = open("mergedSeqs_h1_v4.fna")
#inpH3 = open("mergedSeqs_h3_v4.fna")  #H3 had no fixes to make
outH1 = open("mergedSeqs_h1_v4_nameFix.fna", "w")
#outH3 = open("mergedSeqs_h3_v4_nameFix.fna", "w")





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





h1Dict = ReadFasta(inpH1)
for defline, seq in h1Dict.items():
    if len(seq) > 1:
        print("ERROR1!")
        sys.exit()
    else:
        if defline.startswith("offlu-vcm"):
            defLst = defline.split("|")
            strain = defLst[1]
            strainLst = strain.split("/")
            strainLst[1] = "swine"
            strain = "/".join(strainLst)
            defLst[1] = strain
            
            if "England" in strain:
                if strain == "A/swine/England/237500/2021":
                    date = "2021-04-09"
                elif strain == "A/swine/England/239257/2021":
                    date = "2021-06-18"
                elif strain == "A/swine/England/238879/2021":
                    date = "2021-05-24"
                elif strain == "A/swine/England/237498/2021":
                    date = "2021-04-09"
                elif strain == "A/swine/England/103120/2021":
                    date = "2021-04-29"
                elif strain == "A/swine/England/237596/2021":
                    date = "2021-04-09"
                elif strain == "A/swine/England/238877/2021":
                    date = "2021-05-24"
                elif strain == "A/swine/England/238434/2021":
                    date = "2021-05-13"
                elif strain == "A/swine/England/102081/2021":
                    date = "2021-04-09"
                elif strain == "A/swine/England/102076/2021":
                    date = "2021-04-09"
                elif strain == "A/swine/England/100227/2021":
                    date = "2021"
                
                defLst[-1] = date
                
            defline = "|".join(defLst)
        newlines = ">%s\n%s\n" % (defline, seq[0])
        outH1.write(newlines)
            







inpH1.close()
outH1.close()

















