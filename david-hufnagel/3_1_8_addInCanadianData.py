#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to add canadian sequences to our current data set
and formatting them to fit.
Created by David E. Hufnagel on Jan 11, 2022
"""
import sys

canSeqs = open("canadianSeqs.fna")
inpH1 = open("mergedSeqs_h1_v13.fna")
inpH3 = open("mergedSeqs_h3_v13.fna")
outH1 = open("mergedSeqs_h1_v13_wCAN.fna", "w")
outH3 = open("mergedSeqs_h3_v13_wCAN.fna", "w")





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





#Go through inpH1 and inpH3 and pipe straight to the output
for line in inpH1.readlines():
    outH1.write(line)
    
for line in inpH3.readlines():
    outH3.write(line)


#Go through canSeqs, reformat, and output
canDict = ReadFasta(canSeqs)
for defline, seq in canDict.items():
    if len(seq) > 1:
        print("ERROR!")
        sys.exit()
    else:
        prot = defline.strip().split()[1]
        if prot == "HA":
            defLst = defline.strip().split()[0].split("|")
            strain = defLst[0].replace("_","/")
            subtype = defLst[1]; date = defLst[2]
            
            newlines = ">offlu-vcm|||||||%s|%s|Swine|CAN||%s\n%s\n" % \
                (strain, subtype, date, seq[0])
            
            if subtype.startswith("H1"):
                outH1.write(newlines)
            elif subtype.startswith("H3"):
                outH3.write(newlines)
                












canSeqs.close()
inpH1.close()
inpH3.close()
outH1.close()
outH3.close()









