#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to subsample specific clades from Denmark and date
filter a specific clade from China
Created by David E. Hufnagel on Aug 24, 2020
"""
import sys, random

inp = open(sys.argv[1])
dnkClade1 = open(sys.argv[2])
dnkClade2 = open(sys.argv[3])
dnkClade3 = open(sys.argv[4])
out = open(sys.argv[5], "w")



def Subsample(strainFd, num, goodLst):
    strainLst = []
    for line in strainFd:
        strainLst.append(line.strip())
    
    goodStrains = random.sample(strainLst, num)
    goodLst.extend(goodStrains)
    
    return(goodStrains)
        


#Go through denmark clades and make random selections
goodLst = []
Subsample(dnkClade1, 1, goodLst)
Subsample(dnkClade2, 5, goodLst)
Subsample(dnkClade3, 5, goodLst)

#Go through input and do necessary filtering and subsampling
isGood = True
for line in inp:
    if line.startswith(">"):
        lineLst = line.strip().strip(">").split("|")
        source = lineLst[0]; country = lineLst[5]; date = lineLst[-1]
        clade = lineLst[4]; year = int(date.split("-")[0])
        #Handle China clade
        if source == "publicIAV" and country == "CHN" and clade == "1C.2.3":
            #print(lineLst)
            if year < 2015:
                isGood = False
            else:
                isGood = True
                out.write(line)
        
        #Handle Denmark clades
        elif source in ["publicIAV","offlu"] and country == "DNK" and clade == "1C.2":
            defline = line.strip().strip(">")
            if defline in goodLst:
                isGood = True
                out.write(line)
            else:
                isGood = False
                
        else:
            isGood = True
            out.write(line)
        
    else:
        if isGood:
            out.write(line)








inp.close()
dnkClade1.close()
dnkClade2.close()
dnkClade3.close()
out.close()