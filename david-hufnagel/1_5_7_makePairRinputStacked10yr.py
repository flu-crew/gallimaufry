#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to process a raw data file of pairings between NA and 
HA and generate an output data file which can be used to generate a pairing-
over-time plot in R with the goal of making a stacked line plot with the 10
years data.
Created by David E. Hufnagel on Nov 21, 2020
Updatd on Nov, 2020 to split data by year rather than month
"""
import sys
#from pandas.core.common import flatten
inp = open(sys.argv[1])      #pairData_10yr.txt
out = open(sys.argv[2], "w") #pairData_10yr_RinpStacked_byYear.txt




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
    lineLst = line.strip().split("\t")
    naClade = lineLst[1]; haClade = lineLst[2]  
    nahaPair = "%s_%s" % (naClade, haClade)
    
    date = lineLst[3]; dateLst = date.split("-")
    year = int(dateLst[0])
    inpDict[nahaPair][years.index(year)] += 1


#Write a title for the output
out.write("#python %s\n" % (" ".join(sys.argv)))
out.write("haClade_naClade\tyear\tinstance\n")

#Go through inpDict and output the data in the format:
#  naClade_haClade   year   instance
for nahaPair, yearsCntData in inpDict.items():
    yCnt = 0
    
    for yearCntData in yearsCntData:
        year = years[yCnt]
        hanaPair = "%s_%s" % (nahaPair.split("_")[1], nahaPair.split("_")[0])#flip NA_HA to HA_NA
        newline = "%s\t%s\t%s\n" % (hanaPair, year, yearCntData)
        out.write(newline)
            

        yCnt += 1





inp.close()
out.close()