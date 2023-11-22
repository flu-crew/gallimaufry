#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to add randomly selected individuals to clades with
fewer than 10 strains such that all clades have at least 10 strains.
Created by David E. Hufnagel on Thu Sep  9 09:05:00 2021
"""
import sys, random

inp = open(sys.argv[1])      #allN1s_v4_N1classical_n750a_noOutliers.fna
extra = open(sys.argv[2])    #allN1s_v4_N1classical.fna
out = open(sys.argv[3], "w") #allN1s_v4_N1classical_n750a_noOutliers_fullClades.fna





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
        
        
def RemoveStrain(strain, strainDict):
    for clade, strains in strainDict.items():
        if strain in strains:
            strains.remove(strain)





#Go through extra and make a dict of key: clade val: [strainA, strainB, ...]
#and start the cladeSizeDict with all clades at size 0
cladeSizeDict = {} 
strainDict = {}
for line in extra:
    if line.startswith(">"):
        lineLst = line.strip().split("|")
        clade = lineLst[-3]
        strain = lineLst[1]
        SaveIntoDict(clade, strain, strainDict)
        
        cladeSizeDict[clade] = 0
        
    
#Go through inp and count strains per clade in a dict of key: clade  val: cnt
#   while removing strains from the strainDict and adding them to goodLst. 

goodLst = []
for line in inp:
    if line.startswith(">"):
        lineLst = line.strip().split("|")
        clade = lineLst[-3]
        strain = lineLst[1]
        
        cladeSizeDict[clade] += 1
        
        RemoveStrain(strain, strainDict)

        goodLst.append(strain)
        

#Go through the cladeSizeDict and for clades with fewer than ten strains
#   randomly select enough strains from the strainDict to make 10 strains in
#   each clade and store the result in goodLst
for clade, size in cladeSizeDict.items():
    if size < 10:
        toSample = 10 - size
        newStrains = random.sample(strainDict[clade], toSample)
        for strain in newStrains:
            goodLst.append(strain)


#Go through extra again and output the strains in goodLst
extra.seek(0)
extraDict = ReadFasta(extra)
cnt = 0
for defline, seq in extraDict.items():
    lineLst = defline.strip().split("|")
    strain = lineLst[1]
    if strain in goodLst:
        cnt += 1
        newlines = ">%s\n%s\n" % (defline, seq[0])
        out.write(newlines)





inp.close()
out.close()





