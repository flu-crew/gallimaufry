#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script was designed to take our collection of NA sequences and a large 
set of HA and NA sequences from IRD to produce an output of all paired HA 
sequences found along with a list of strain names for sequences not found
Created by David E. Hufnagel on Apr 29, 2022
"""
import sys
nasFd = open("allN1s_v4.fna")
bigDataFd = open("hAandNAall.fasta")
pairedHAout = open("mostHAs.fna", "w")
missingNAout = open("missingNAs.txt", "w")





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





#Go through nasFd and make a list of present strain names as well as a dict of
#key: strain  val: defline
nasDict = ReadFasta(nasFd)
strainDict = {}
naStrains = []
for defline, seq in nasDict.items():
    strain = defline.split("|")[1].replace("swine","Swine").replace(" ","_")
    strainDict[strain] = defline
    naStrains.append(strain)
#print("A/Swine/North_Carolina/02084/2008" in strainDict)
#print("A/Swine/North_Carolina/02084/2008" in naStrains)

#Go through bigDataFd and collect all HA sequences related to NA strain names,
#  while removing names from  the list.  At the end output all unpaired 
#  NA strains
bigDataDict = ReadFasta(bigDataFd)
for defline, seq in bigDataDict.items():
    segment = int(defline.split("|")[2])
    if segment == 4:
        strain = defline.split("|")[0].replace("swine","Swine").replace(" ","_")
        if strain == "A/Swine/North_Carolina/02084/2008":
            print(defline)
        if strain in strainDict:
            defline = strainDict[strain]
            newlines = ">%s\n%s\n" % (defline, seq[0])
            pairedHAout.write(newlines)
            #print(strain)
            naStrains.remove(strain)
    ## THERE ARE SEVERAL DUPLICATES IN THE BIG DATA SET THAT NEED TO BE REMOVED ##
     
#print(naStrains)
#print(len(naStrains))







nasFd.close()
bigDataFd.close()
pairedHAout.close()
missingNAout.close()