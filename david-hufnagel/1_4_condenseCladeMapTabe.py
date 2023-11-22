#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script was designed to take a table with strain-level information and 
condense it to reflecting information about clades by month
Created by David E. Hufnaegl on Aug 30. 2020
"""
import sys

inp = open("country-global_clade-map-2020Sept.txt")
out = open("country-global_clade-map-2020Sept_condensed.txt", "w")



def SaveIntoNumDict(key, dictx):
    if key in dictx:
        dictx[key] += 1
    else:
        dictx[key] = 1
        
def ConvertYear(old):
    if old == "18":
        new = "2018"
    elif old == "19":
        new = "2019"
    elif old == "20":
        new = "2020"
    else:
        print("ERROR!")
        sys.exit()
        
    return(new)



#Go through input and make a dict of key: subtype-country-clade-year-month 
#  val: cnt
cladeDict = {}
inp.readline()
for line in inp:
    lineLst = line.strip().split("\t")
    subtype = lineLst[1]; cntry = lineLst[2]; clade = lineLst[3]
    date = lineLst[4]
    year = ConvertYear(date.split("/")[2])
    month = date.split("/")[0]
    bigName = "%s_%s_%s_%s_%s" % (subtype, cntry, clade, year, month.zfill(2))
    SaveIntoNumDict(bigName, cladeDict)


#Write title line
newline = "Subtype\tCountry\tClade\tYear-Month\tCount\n"
out.write(newline)


#Go through this dict and output the results in the format:
#  subtype  country  clade  year-month  count
for bigName, cnt in cladeDict.items():
    bigLst = bigName.split("_")
    subtype = bigLst[0]; cntry = bigLst[1]; clade = bigLst[2]
    year = bigLst[3]; month = bigLst[4]
    newline = "%s\t%s\t%s\t%s-%s\t%s\n" % (subtype, cntry, clade, year, month, cnt)
    out.write(newline)





inp.close()
out.close()