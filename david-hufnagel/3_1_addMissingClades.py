#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to use octoFLU classifier data to add clade info
to an OFFLU fasta where it is missing.

Created by David E. Hufnagel on Dec 28, 2021
"""
import sys

inp = open("mergedSeqs_v1_noDups.fna")
classFD = open("mergedSeqs_v1_noDups.fna_Final_Output.txt")
outH1 = open("mergedSeqs_v1_noDups_allClades_h1.fna", "w")
outH3 = open("mergedSeqs_v1_noDups_allClades_h3.fna", "w")





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





#Go through classFD and make a dict of key: strain val: clade
cladeDict = {}
for line in classFD:
    lineLst = line.split("\t")
    strain = "_".join(lineLst[0].split("_")[1:-5])
    clade = lineLst[-2].replace("-vaccine","").replace("humanVaccine","")
    cladeDict[strain] = clade
    

#Go through inp, fill in missing clade info, and pipe to output splitting
#   H1 and H3
inpDict = ReadFasta(inp)
for defline, seq in inpDict.items():
    if len(seq) > 1:
        print("ERROR!")
        sys.exit()
    else:
        defLst = defline.split("|"); strain = defLst[1]
        clade = defLst[-2]; subtype = defLst[2]
        
        if strain not in ["A/Pigeon/Turkey/21/2006"]:
            if clade in [""," ","humanVaccine"]:
                clade = cladeDict[strain]
                
        defLst[-2] = clade
        newdef = "|".join(defLst)
        newlines = ">%s\n%s\n" % (newdef, seq[0])     

        if subtype.startswith("H1"):
            outH1.write(newlines)
        elif subtype.startswith("H3"):
            outH3.write(newlines)






inp.close()
classFD.close()
outH1.close()
outH3.close()










