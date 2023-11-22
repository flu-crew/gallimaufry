#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take a file containing sequences of interest and
another file which links to HA accession data and make a list of accessions
with one accession per line
Created by David E. Hufnagel on Thu Apr  8 16:32:00 2021
"""
import sys

accFd = open("AC_viruses_swine_sera_standardization-updated_20201118_normal.txt")
strainFd = open("616C-all-distances.csv")
out = open("616C-all-distances_antigens_accs.txt", "w")



def SaveIntoDict(key, val, dictx):
    if key in dictx:
        dictx[key].append(val)
    else:
        dictx[key] = [val,]



#Go through strainFd and capture all relevant strain names
strainFd.readline()
names = set([])
for line in strainFd:
    lineLst = line.strip().split(",")
    if "SR" not in lineLst[0] + lineLst[2]:
        names.add(" ".join(lineLst[1].split(" ")[:-1]))
        names.add(" ".join(lineLst[3].split(" ")[:-1]))


#Go through accFd and make a dict of key: strain  val: HAacc for all variations
#of the strain names
accDict = {}
accFd.readline()
for line in accFd:
    lineLst = line.strip().split("\t")
    if lineLst == [""]:
        break
    
    acc = lineLst[11]
    SaveIntoDict(lineLst[0].upper(), acc, accDict)
    
#cleanup dict so that theer's only one accession per strain name
accDict2 = {}
for key,val in accDict.items():
    if len(set(val)) > 1:
        for acc in set(val):
            if acc in ["CY163512", "GQ149689", "CY099119", "CY098468"]:
                accDict2[key] = acc
    else:
        accDict2[key] = val[0]
        

#Go through the names, look for matches in the accDict and output accessions
for name in names:
    if not name in accDict.keys():
        if not name.replace(" ", "_") in accDict.keys():
            if name == "A/SWINE/MANITOBA/D0392/2014":
                newname = "A/SWINE/MANITOBA/D0392/2015"
                acc = accDict2[newname]
            elif name == "A/USSR/1977":
                newname = "A/USSR/90/1977"
                acc = accDict2[newname]
            elif name == "A/SOLOMON ISLAND/3/2006":
                newname = "A/Solomon Islands/3/2006".upper()
                acc = accDict2[newname]
            elif name == "A/SINGAPORE/1986":
                newname = "A/Singapore/6/1986".upper()
                acc = accDict2[newname]
            elif name == "A/SWINE/OHIO/511445/2007":
                newname = "A/swine/OH/511445/2007".upper()
                acc = accDict2[newname]
                
            if name == "A/CALIFORNIA/4/2009":
                acc = "MN371616"
            elif name == "A/SWINE/MANITOBA/SD0102/2015":
                acc = "MF768539"
            elif name == "A/SWINE/SASKATCHEWAN/SD0200/2015":
                acc = "MF768547"
        else:
            acc = accDict2[name.replace(" ", "_")]
    else:
        acc = accDict2[name]

    #Clean up where acc listed isn't in genbank
    if acc == "EPI_ISL_90277":
        acc = "D00407"
    elif acc == "CY125100":
        acc = "CY033622"
    elif acc == "EPI760602":
        acc = "KX949404"
        
    #output to file
    newline = "%s\n" % (acc)
    out.write(newline)






accFd.close()
strainFd.close()
out.close()