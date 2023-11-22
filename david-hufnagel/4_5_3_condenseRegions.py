#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script takes a tabular R input file on the regions where gamma clades are
found and condenses it so there are fewer categories and therefore fewer 
colors to try to disninguish
Created by David E. Hufnagel on  Aug 22, 2023
"""
import sys

inp = open(sys.argv[1])      #gammaSeqs_v3_nameFix_regData.tab
out = open(sys.argv[2], "w") #gammaSeqs_v3_nameFix_regData_cond.tab





def SaveIntoCntDict(key, dictx):
    if key in dictx:
        dictx[key] += 1
    else:
        dictx[key] = 1
        
def SaveIntoCntDict2(key, dictx, cnt):
    if key in dictx:
        dictx[key] += cnt
    else:
        dictx[key] = cnt

def ConvertReg(reg): #The regions were combined in the end
    if reg in ["MS","OK","VA","TX","AR","KY","SC","GA","TN","AL","FL"]:
        newReg = "OtherUSA"
    elif reg in ["MI","KS","WI","ND"]:
        newReg = "OtherUSA"
    elif reg in ["PA"]:
        newReg = "OtherUSA"
    elif reg in ["CO","WY","CA","AZ","UT"]:
        newReg = "OtherUSA"
    else:
        newReg = reg
    return(newReg)
        
        
        

#Go through inp and make a dict of key: region  val: cnt
oldRegDict = {}
for line in inp:
    lineLst = line.strip().split("\t")
    reg = lineLst[-1]
    SaveIntoCntDict(reg, oldRegDict)


#Go through regionDict and make dict with new, condensed regions, newRegDict.
#T  his second dict is used only to make decisions.
newRegDict = {}
for reg, cnt in oldRegDict.items():
    newReg = ConvertReg(reg)
    SaveIntoCntDict2(newReg, newRegDict, cnt)
print(newRegDict)


#Go through inp again, replace old region with new region, and output result
inp.seek(0)
for line in inp:
    lineLst = line.strip().split("\t")
    newReg = ConvertReg(lineLst[-1])
    lineLst[-1] = newReg
    newline = "\t".join(lineLst) + "\n"
    out.write(newline)






inp.close()
out.close()