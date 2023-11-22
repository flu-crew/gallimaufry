#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to add an "US_Other" category to our region data to 
solve the problem of having too many different regions to tell them apart on
the stacked bar chart.  US_unknown and regions with 50 or fewer strains are
set to this other category.
Created by David E. Hufnagel on Wed Apr  7 10:16:51 2021
"""
import sys


inp = open(sys.argv[1])      #allN1s_v4_regData.tab
out = open(sys.argv[2], "w") #allN1s_v4_regData2.tab



def SaveIntoCntDict(key, dictx):
    if key in dictx:
        dictx[key] += 1
    else:
        dictx[key] = 1
        
def SaveIntoSumDict(key, val, dictx):
    if key in dictx:
        dictx[key] += val
    else:
        dictx[key] = val



#Go through the input file and store region counts in a dict
regionDict = {}
for line in inp:
    lineLst = line.strip().split("\t")
    SaveIntoCntDict(lineLst[2], regionDict)


#Go through that dict and make a dict of key: oldRegion  val: newRegion, 
#  where the new region is sometimes the old one and is sometimes "US_Other"
# test = {}
# for region, cnt in regionDict.items():
#     if region == "US_unknown" or cnt <= 50:
#         SaveIntoSumDict("US_other", cnt, test)
#     else:
#         test[region] = cnt
        
# print(len(regionDict.keys()))
# print(regionDict)
# print()
# print(len(test.keys()))
# print(test)

translateDict = {}
for region, cnt in regionDict.items():
    if region == "US_unknown" or cnt <= 50:
        translateDict[region] = "Other"
    else:
        translateDict[region] = region


#Go through the input file again and ouput the file with new region assignments
inp.seek(0)
for line in inp:
    lineLst = line.strip().split("\t")
    lineLst[2] = translateDict[lineLst[2]]
    newline = "\t".join(lineLst) + "\n"
    out.write(newline)







inp.close()
out.close()