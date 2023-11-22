#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to filter most USA sequences before 2021 out of the
data set (all references are retained). Also imposes a similar before 2017
for non-US sequences.
Created by David E. Hufnagel on Jan  5, 2022
"""
import sys

inpH1 = open("mergedSeqs_h1_v10_newCons_clean.fna")
inpH3 = open("mergedSeqs_h3_v10.fna")
outH1 = open("mergedSeqs_h1_v10_newCons_clean_USdateFilt.fna", "w")
outH3 = open("mergedSeqs_h3_v10_USdateFilt.fna", "w")





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





#Go through H1, filter out old non-reference seqs and output
h1Dict = ReadFasta(inpH1)
for defline, seq in h1Dict.items():
    if len(seq) < 1:
        print("ERROR1!")
        sys.exit()
    else:
        defLst = defline.strip().split("|")
        prov = defLst[0]
        date = defLst[-1]
        if "onsensus" not in defline:
            year = int(date.split("-")[0])
            cntry = defLst[-3]
        else:
            year = 0; cntry = 0
            
        if not (("onsensus" not in defline and "lab-" not in defline and prov in ["offlu-vcm","publicIAV"] \
            and cntry == "USA" and year < 2021) or \
            ("onsensus" not in defline and "lab-" not in defline and prov in ["offlu-vcm","publicIAV"] \
             and cntry != "USA" and year < 2017)): #to keep
            newlines = ">%s\n%s\n" % (defline, seq[0])
            outH1.write(newlines)


#Go through H3, filter out old non-reference seqs and output
h3Dict = ReadFasta(inpH3)
for defline, seq in h3Dict.items():
    if len(seq) < 1:
        print("ERROR2!")
        sys.exit()
    else:
        defLst = defline.strip().split("|")
        prov = defLst[0]
        date = defLst[-1]
        if "onsensus" not in defline:
            year = int(date.split("-")[0])
            cntry = defLst[-3]
        else:
            year = 0; cntry = 0
            
        if not (("onsensus" not in defline and "lab-" not in defline and prov in ["offlu-vcm","publicIAV"] \
            and cntry == "USA" and year < 2021) or \
            ("onsensus" not in defline and "lab-" not in defline and prov in ["offlu-vcm","publicIAV"] \
             and cntry != "USA" and year < 2017)): #to keep
            newlines = ">%s\n%s\n" % (defline, seq[0])
            outH3.write(newlines)










inpH1.close()
inpH3.close()
outH1.close()
outH3.close()








