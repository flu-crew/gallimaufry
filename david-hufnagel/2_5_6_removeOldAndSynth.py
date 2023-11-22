#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to filter H1 and H3 OFFLU files by date, removing
strains before 2016 except for various kinds of reference strains.  It also
removes a specific set of synthetic strains and related reference sequences
from the H3 file.
Created by David E. Hufnagel on Wed Aug 18 20:35:32 2021
"""
import sys
inpH1 = open("mergedSeqs_v13_h1.fna")
inpH3 = open("mergedSeqs_v14_h3_wE72_1990restore.fna")
outH1 = open("mergedSeqs_v14_h1.fna", "w")
outH3 = open("mergedSeqs_v15_h3.fna", "w")

SYNTH_BAD = ["syntheticIAV||||||A/swine/Chachoengsao/NIAH117865-042/2017|H3N2|Swine|THA|3.1990.3|2017-07-05", \
             "synth-ref||||||A/swine/Chachoengsao/NIAH117865-033/2017|H3N2|Swine|THA|3.1990.3|2017-07-05", \
                 "synth-ref||||||A/swine/Thailand/CU-S14252N/2014|H3N2|Swine|THA|3.1990.3|2014-01-20", \
                     "synth-ref||||||A/swine/Thailand/CU22337/2018|H3N2|Swine|THA|3.1990.3|2018-10-01", \
                         "syntheticIAV||||||A/swine/China/JG20/2019|H3N2|Swine|CHN|3.2000.4|2019-01", \
                             "syntheticIAV||||||A/swine/094-18/Brazil/2018|H3N2|Swine|BRA|3.1990.5|2018", \
                                 "synth-ref||||||A/swine/Brazil/360-17/2017|H3N2|Swine|BRA|3.1990.5|2017-08-30", \
                                     "synth-ref||||||A/swine/Brazil/068_15/2015|H3N2|Swine|BRA|3.1990.5|2015-04-01", \
                                         "syntheticIAV||||||A/swine/091-18-2/Brazil/2018|H3N2|Swine|BRA|3.1990.5|2018", \
                                             "synth-ref||||||A/swine/Brazil/527-17/2017|H3N2|Swine|BRA|3.1990.5|2017-09-28", \
                                                 "synth-ref||||||A/swine/Brazil/154_14-1/2014|H3N2|Swine|BRA|3.1990.5|2014-08-01"]

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




    
#Go through inpH1, filter by date and provenance, and output the result
inpH1Dict = ReadFasta(inpH1)
for defline, seq in inpH1Dict.items():
    if len(seq) == 1:
        defLst = defline.strip().strip(">").split("|")
        prov = defLst[0]
        
        if prov in ["CVV", "SwReference", "huReference", "huVaccine", "synth-ref", "syntheticIAV", "variant"]: #for some provenances keep everything
            isGood = True
        elif prov in ["offlu-vcm", "publicIAV"]:  #Make a decision for these strains
            date = defLst[-1]
            year = int(date.split("-")[0])
            if year > 2015:
                isGood = True
            else:
                isGood = False
        else:
            print("ERROR 2!")
            sys.exit()
            
        if isGood:
            newlines = ">%s\n%s\n" % (defline, seq[0])
            outH1.write(newlines)
            
    else:
        print("ERROR 1!")
        sys.exit()

    
#Go through inpH3, filter by date and provenance, exclude SYNTH_BAD strains,
#   and output the result
inpH3Dict = ReadFasta(inpH3)
for defline, seq in inpH3Dict.items():
    if len(seq) == 1:
        defLst = defline.strip().strip(">").split("|")
        prov = defLst[0]
        date = defLst[-1]
        year = int(date.split("-")[0])
        if defline in SYNTH_BAD:
            isGood = False
        elif year > 2015:
            isGood = True
        elif prov in ["CVV", "SwReference", "huReference", "huVaccine", "synth-ref", "syntheticIAV", "variant"]:
            isGood = True
        else:
            isGood = False
            
    else:
        print("ERROR 2!")
        sys.exit()
    
    if isGood:
        newlines = ">%s\n%s\n" % (defline, seq[0])
        outH3.write(newlines)
    
    
    
    
    
    
inpH1.close(); inpH3.close(); outH1.close(); outH3.close()