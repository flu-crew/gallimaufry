#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to process a raw data file of pairings between NA and 
HA and generate an output data file which can be used to generate a pairing-
over-time plot in R with the goal of making a stacked line plot with the 10
years data.
Created by David E. Hufnagel on Nov 21, 2020
"""
import sys
#from pandas.core.common import flatten
inp = open(sys.argv[1])      #pairData_10yr.txt
out = open(sys.argv[2], "w") #pairData_10yr_RinpStacked.txt



def MakeYearsLst(years):
    yearsLst = []
    for year in years:
        yearLst = [0,0,0,0,0,0,0,0,0,0,0,0]
        yearsLst.append(yearLst)
        
    return(yearsLst)


# def GetPair(monthLst, allHAs):
#     pairData = []
#     for clade in allHAs:
#         if len(monthLst) == 0:
#             perClade = "NA"
#         else:
#             perClade = float(monthLst.count(clade)) / float(len(monthLst))
#         pairData.append((clade, perClade))
        
#     return(pairData)
    
# def CollectHAs(inpDict):
#     haDict = {}
#     for naClade, yearsLst in inpDict.items():
#         allHAs = list(set((flatten(yearsLst))))
        
#         haDict[naClade] = allHAs
        
#     return(haDict)




#Go through input file once to determine what years and NAclade_HAclade 
#  combinations are present in the data set
years = set([])
nahaClades = set([])
for line in inp:
    lineLst = line.strip().split("\t")
    date = lineLst[3]; dateLst = date.split("-")
    year = int(dateLst[0])
    years.add(year)
    
    naClade = lineLst[1]; haClade = lineLst[2]
    nahaPair = "%s_%s" % (naClade, haClade)
    nahaClades.add(nahaPair)
    
years = list(years); years.sort()
nahaClades = list(nahaClades); nahaClades.sort()


#Go through nahaPairLst and start the inpDict (of key: NAclade_HAclade 
#  val: [Year1Lst, Year2st...] where each list is a list of counts per month 
#  of sequences with that clade combination) with empty values
inpDict = {}
for pair in nahaClades:
    yearsLst = MakeYearsLst(years)
    inpDict[pair] = yearsLst
    

#Go through input file and fill in inpDict with data
inp.seek(0)
for line in inp:
    lineLst = line.strip().split("\t")
    naClade = lineLst[1]; haClade = lineLst[2]  
    nahaPair = "%s_%s" % (naClade, haClade)
    
    date = lineLst[3]; dateLst = date.split("-")
    year = int(dateLst[0])
    if len(dateLst) != 1:
        month = int(dateLst[1])
    else:
        month = "NA"

    if month != "NA":
        inpDict[nahaPair][years.index(year)][month-1] += 1


#Write a title for the output
out.write("#python %s\n" % (" ".join(sys.argv)))
out.write("naClade_haClade\tyear\tmonth\tmonthNum\tinstance\n")

#Go through inpDict and output the data in the format:
#  naClade_haClade   year   month   monthNum   instance
for nahaPair, yearsCntData in inpDict.items():
    yCnt = 0
    for yearCntData in yearsCntData:
        mCnt = 1
        for monthStrainCnt in yearCntData:
            year = years[yCnt]
            monthNum = yCnt * 12 + mCnt 
            if monthNum < 130:  #cut off R input where there is no data
                newline = "%s\t%s\t%s\t%s\t%s\n" % \
                    (nahaPair, year, mCnt, monthNum, monthStrainCnt)
            out.write(newline)
            
            mCnt += 1
        yCnt += 1





inp.close()
out.close()