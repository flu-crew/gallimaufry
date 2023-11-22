#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designde to take a fasta file for OFFLU containing only H1
data and split it into 1A, 1B, and 1C
Created by David E. Hufnagel on Mon Jul 19 10:38:19 2021
"""
import sys
inp = open("mergedSeqs_v7_h1_minChileRef.fna")
out1A = open("mergedSeqs_v7_h1_1A.fna", "w")
out1B = open("mergedSeqs_v7_h1_1B.fna", "w")
out1C = open("mergedSeqs_v7_h1_1C.fna", "w")





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





#Go through the input, split by clade, then output
inpDict = ReadFasta(inp)
for defline, seq in inpDict.items():
    defLst = defline.split("|")
    clade = defLst[-2]
    cntry = defLst[-3]
    strain = defLst[-6]
    
    #determine the lineage
    if clade.startswith("1A"):
        lineage = "1A"
    elif clade.startswith("1B"):
        lineage = "1B"
    elif clade.startswith("1C"):
        lineage = "1C"
    else:
        if cntry == "JPN":
            clade = "1A"
            lineage = "1A"
        elif "Other-Human" not in clade:
            if strain in ["A/Wisconsin/03/2021", "A/Denmark/1/2021", "A/Iowa/02/2021", "A/Manitoba/01/2021", "A/Manitoba/02/2021", "A/North_Carolina/15/2020"]:
                lineage = "1A"
                if strain  == "A/North_Carolina/15/2020":
                    clade = "1A.3.3.3"
                else:
                    clade = "1A.3.3.2"
            elif strain in ["A/Mecklenburg-Vorpommern/1/2021", "A/swine/Shandong/POS2539/2015"]:
                lineage = "1C"
                if strain == "A/Mecklenburg-Vorpommern/1/2021":
                    clade = "1C.2.1"
                else:
                    clade = "1C.2.3"
            else:
                print("ERROR 1!")
                sys.exit()
        else:
            lineage = "1B"
            
    #output data
    if len(seq)  == 1:
        defLst[-2] = clade
        newDef = "|".join(defLst)
        if lineage == "1A":
            newlines = ">%s\n%s\n" % (newDef, seq[0])
            out1A.write(newlines)
        elif lineage == "1B":
            newlines = ">%s\n%s\n" % (newDef, seq[0])
            out1B.write(newlines)
        elif lineage == "1C":
            newlines = ">%s\n%s\n" % (newDef, seq[0])
            out1C.write(newlines)
        else:
            print("ERROR 2!")
            sys.exit()
    else:
        print("ERROR 3!")
        sys.exit()

















inp.close()
out1A.close()
out1B.close()
out1C.close()