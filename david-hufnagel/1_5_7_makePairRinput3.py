#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to process a raw data file of pairings between NA and 
HA and generate an output data file which can be used to generate a pairing-
over-time plot in R
Created by David E. Hufnagel on Nov 10, 2020
Updated on Nov 17, 2020 to accomidate the 10 years data set
Updated on Jan 6, 2021 to add region information 
"""
import sys
from pandas.core.common import flatten
inp = open(sys.argv[1])      #pairData_10yr.txt
out = open(sys.argv[2], "w") #pairData_10yr_Rinp.txt



def MakeYearsLst(years):
    yearsLst = []
    for year in years:
        yearLst = [[],[],[],[],[],[],[],[],[],[],[],[]]
        yearsLst.append(yearLst)
        
    return(yearsLst)


def GetPair(monthLst, allHAs):
    pairData = []
    for clade in allHAs:
        if len(monthLst) == 0:
            perClade = "NA"
            count = "NA"
        else:
            count = float(monthLst.count(clade))
            perClade = count / float(len(monthLst))
        
        pairData.append((clade, count, perClade))
        
    return(pairData)
    
def CollectHAs(inpDict):
    haDict = {}
    for naClade, yearsLst in inpDict.items():
        allHAs = list(set((flatten(yearsLst))))
        
        haDict[naClade] = allHAs
        
    return(haDict)




#Go through input file once to determine what years are present in the data set
years = set([])
for line in inp:
    if not line.startswith("#"):
        lineLst = line.strip().split("\t")
        date = lineLst[-1]; dateLst = date.split("-")
        year = int(dateLst[0])
        years.add(year)
years = list(years)
years.sort()


#Go through input file and build a dict of key: NA clade val: [Year1Lst,
#  Year2st...] where each list is a list of HA clades represented in each month
#  with one entry per istance
inpDict = {}
inp.seek(0)
for line in inp:
    if not line.startswith("#"):
        lineLst = line.strip().split("\t")
        naClade = lineLst[1]; haClade = lineLst[2]    
        
        date = lineLst[-1]; dateLst = date.split("-")
        year = int(dateLst[0])
        if len(dateLst) != 1:
            month = int(dateLst[1])
        else:
            month = "NA"
            
        if naClade not in inpDict:
            yearsLst = MakeYearsLst(years)
            inpDict[naClade] = yearsLst
    
        if month != "NA":
            inpDict[naClade][years.index(year)][month-1].append(haClade)

#Collect all HA clades to fill in empty months with zeroes later
haDict = CollectHAs(inpDict)


#Go through dict, calculate percentages for each month and create an output
#  in the format:  naClade   haClade   year   month   monthNum   region   %pair
for naClade, yearsLst in inpDict.items():
    yCnt = 0
    for yearLst in yearsLst:
        year = years[yCnt]
        mCnt = 1
        
        for monthLst in yearLst:  
            pairData = GetPair(monthLst, haDict[naClade])
            monthNum = yCnt * 12 + mCnt                        

            for pair in pairData:
                haClade = pair[0]; cntHA = pair[1]; perHA = pair[2]
                if monthNum < 130:  #cut off R input where there is no data
                    newline = "%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (naClade, haClade, year, mCnt, monthNum, cntHA, perHA)
                    out.write(newline)
            
            mCnt += 1
        
        yCnt += 1            
        



inp.close()
out.close()