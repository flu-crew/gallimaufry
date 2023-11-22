#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to combine all human IAV sequences from the last 12
months with all HA octoFLU references.
Created by David E. Hufnagel on Wed Jul 14 16:02:10 2021
"""
import sys

humanFasta = open("human-12-month-context.fna")
swineFasta = open("octoFLUrefs.fna")
outH1 = open("combinedData_H1.fna", "w")
outH3 = open("combinedData_H3.fna", "w")




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





#Go through human data and pipe it straight to the output
humanDict = ReadFasta(humanFasta)
for defline, seq in humanDict.items():
    subtype = defline.split("|")[2]
    
    if len(seq) == 1:
        if subtype in ["H1N1","H1N2"]:
            newlines = ">%s\n%s\n" % (defline, seq[0])
            outH1.write(newlines)
        elif subtype in ["H3N2"]:
            newlines = ">%s\n%s\n" % (defline, seq[0])
            outH3.write(newlines)
    else:
        print("ERROR 1!")
        sys.exit()
    

#Go through swine data, keep only HA seqs and pipe them to the output
swineDict = ReadFasta(swineFasta)
for defline, seq in swineDict.items():
    segment = defline.split("|")[4]
    
    if len(seq) == 1:
        if segment == "H1":
            newlines = ">%s\n%s\n" % (defline, seq[0])
            outH1.write(newlines)
        elif segment == "H3":
            newlines = ">%s\n%s\n" % (defline, seq[0])
            outH3.write(newlines)
    else:
        print("ERROR 2!")
        sys.exit()












humanFasta.close()
swineFasta.close()
outH1.close()
outH3.close()