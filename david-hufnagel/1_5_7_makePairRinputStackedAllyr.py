#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to process a raw data file of pairings between NA and 
HA and generate an output data file which can be used to generate a pairing-
over-time plot in R with the goal of making a stacked line plot with the 10
years data.
Created by David E. Hufnagel on Nov 21, 2020
Updated on Feb 3, 2021 to use all years data
"""
import sys
inp = open(sys.argv[1])      #pairData_Ayr.txt
out = open(sys.argv[2], "w") #pairData_Ayr_RinpStacked_byYear.txt




#Go through input file once to determine what years and NAclade_HAclade 
#  combinations are present in the data set
years = set([])
nahaClades = set([])
for line in inp:
    if not line.startswith("#"):
        lineLst = line.strip().split("\t")
        date = lineLst[-1]; dateLst = date.split("-")
        year = int(dateLst[0])
        years.add(year)
        
        naClade = lineLst[1]; haClade = lineLst[2]
        nahaPair = "%s_%s" % (naClade, haClade)
        nahaClades.add(nahaPair)
    
nahaClades = list(nahaClades); nahaClades.sort()


#Add missing years between the largest and smallest year values
oldest = min(years)
newest = max(years)
years = []
for i in range(oldest, newest + 1):
    years.append(i)


#Go through nahaPairLst and start the inpDict (of key: NAclade_HAclade 
#  val: [Year1Lst, Year2st...] where each list is a list of counts per year
#  of sequences with that clade combination) with empty values
inpDict = {}
for pair in nahaClades:
    yearsLst = []
    for year in years:
        yearsLst.append(0)
        
    inpDict[pair] = yearsLst
    
    
#Go through input file and fill in inpDict with data
inp.seek(0)
for line in inp:
    if not line.startswith("#"):
        lineLst = line.strip().split("\t")
        naClade = lineLst[1]; haClade = lineLst[2]  
        nahaPair = "%s_%s" % (naClade, haClade)
        
        date = lineLst[-1]; dateLst = date.split("-")
        year = int(dateLst[0])
        inpDict[nahaPair][years.index(year)] += 1


#Write a title for the output
out.write("#python %s\n" % (" ".join(sys.argv)))
out.write("haClade_naClade\tyear\tinstance\tnaClade\n")

#Go through inpDict and output the data in the format:
#  naClade_haClade   year   instance
for nahaPair, yearsCntData in inpDict.items():
    yCnt = 0
    
    for yearCntData in yearsCntData:
        year = years[yCnt]
        naClade = nahaPair.split("_")[0]
        haClade = "_".join(nahaPair.split("_")[1:])
        hanaPair = "%s_%s" % (haClade, naClade)#flip NA_HA to HA_NA
        newline = "%s\t%s\t%s\t%s\n" % (hanaPair, year, yearCntData, naClade)
        out.write(newline)
            

        yCnt += 1





inp.close()
out.close()