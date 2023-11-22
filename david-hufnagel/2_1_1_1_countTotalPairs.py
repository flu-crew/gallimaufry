#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take a file with NA-HA pair information split by 
year and combine it into NA-HA pair info that is not split at all in order 
to get a better understanding of the total volume of pairs in the data.
Created by David E. Hufnagel on Wed Jan  6 14:35:57 2021
"""
import sys

inp = open(sys.argv[1])
out = open(sys.argv[2], "w")



def SaveIntoNumDict(key, val, dictx):
    if key in dictx:
        dictx[key] += val
    else:
        dictx[key] = val
        
        

#Go through inp and make a dict of key: HA_NA  val: cnt
pairsDict = {}
inp.readline(); inp.readline()
for line in inp:
    lineLst = line.strip().split("\t")
    SaveIntoNumDict(lineLst[0], int(lineLst[2]), pairsDict)


    
#Go through pairsDict and output data
for pair, cnt in pairsDict.items():
    newline = "%s\t%s\n" % (pair, cnt)
    out.write(newline)








inp.close()
out.close()
