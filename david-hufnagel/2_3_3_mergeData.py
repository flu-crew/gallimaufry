#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to combine aadiff information and HI information
into one file.
Created by David E. Hufnagel on Tue Apr 13 12:17:35 2021
"""
import sys

aaDiffs = open(sys.argv[1])  #gammaAAdifs_Apr13.csv
hiDiffs = open(sys.argv[2])  #616C-all-distances.csv
out = open(sys.argv[3], "w") #gamma_compareAAdiffHIdiff.tab



def ChangeStrainNames(old):
    if old == "A/OHIO/09/2015":
        return("A/OHIO/9/2015")
    elif old == "A/CALIFORNIA/04/2009":
        return("A/CALIFORNIA/4/2009")
    elif old == "A/MINNESOTA/45/2015":
        return("A/MINNESOTA/45/2016")
    elif old == "A/SWINE/MANITOBA/D0392/2015":
        return("A/SWINE/MANITOBA/D0392/2014")
    elif old == "A/SWINE/OH/511445/2007":
        return("A/SWINE/OHIO/511445/2007")
    elif old == "A/SWINE/SASKATCHEWAN/SD0102/2015":
        return("A/SWINE/MANITOBA/SD0102/2015")
    elif old == "A/SWINE/SASKATCHEWAN/SD0200/2016":
        return("A/SWINE/SASKATCHEWAN/SD0200/2015")
    else:
        return(old)




#Go through aaDiffs and save aadif data in a dict of key: strainA_strainB  val: aaDiff
##Save strain names from the title in a list.  Also make a dict of key: strain  val: clade
aaDtitle = aaDiffs.readline()
aaDtList = aaDtitle.strip().split(",")
strains = []; cladeDict = {}
for strain in aaDtList:
    if strain != "":
        strains.append(strain.split("|")[0].upper())
        clade = strain.split("|")[4]
        cladeDict[strain] = clade
        
##Collect aaDif data
aaDiffDict = {}
for line in aaDiffs:
    lineLst = line.strip().split(",")
    strainA = lineLst[0].split("|")[0].upper()
    
    cnt = 0
    for val in lineLst[1:]:
        strainB = strains[cnt].upper()
        
        #change strain names to match what is in the HI data table
        strainA = ChangeStrainNames(strainA)
        strainB = ChangeStrainNames(strainB)
        key = "%s_%s" % (strainA.upper(), strainB.upper())
        
        #except for blank values convert from aa similarity to aa dist
        if val != "":
            val = str(100 - float(val))
        aaDiffDict[key] = val
        
        cnt += 1
    
    
#Go through strains and modify names to match what is found in hiDiffs
strains2 = []
for strain in strains:
    if strain == "A/OHIO/09/2015":
        strains2.append("A/OHIO/9/2015")
    elif strain == "A/CALIFORNIA/04/2009":
        strains2.append("A/CALIFORNIA/4/2009")
    elif strain == "A/MINNESOTA/45/2015":
        strains2.append("A/MINNESOTA/45/2016")
    elif strain == "A/SWINE/MANITOBA/D0392/2015":
        strains2.append("A/SWINE/MANITOBA/D0392/2014")
    elif strain == "A/SWINE/OH/511445/2007":
        strains2.append("A/SWINE/OHIO/511445/2007")
    elif strain == "A/SWINE/SASKATCHEWAN/SD0102/2015":
        strains2.append("A/SWINE/MANITOBA/SD0102/2015")
    elif strain == "A/SWINE/SASKATCHEWAN/SD0200/2016":
        strains2.append("A/SWINE/SASKATCHEWAN/SD0200/2015")
    else:
        strains2.append(strain)
    
    

#Write the title to the output
title = "ID1\tStrain1\tID2\tStrain2\tHIdist\taaDist(%)\n"
out.write(title)


#Go through hiDiffs, match strain names, and output all data for relevant 
#  strains.  Also remove strains from the strains list as we go to see if all
#  are encountered
hiDiffs.readline()
for line in hiDiffs:
    lineLst = line.strip().split(",")
    if not "SR" in lineLst[0] + lineLst[2]:
        strainA = " ".join(lineLst[1].split(" ")[:-1]).replace(" ", "_")
        strainB = " ".join(lineLst[3].split(" ")[:-1]).replace(" ", "_")
        key1 = "%s_%s" % (strainA, strainB)
        key2 = "%s_%s" % (strainB, strainA)
        if key1 in aaDiffDict:
            if strainA in strains2:
                strains2.remove(strainA)
            if strainB in strains2:
                strains2.remove(strainB)
                
            newline = "%s\t%s\t%s\t%s\t%s\t%s\n" % \
                (lineLst[0], lineLst[1], lineLst[2], lineLst[3], lineLst[4], aaDiffDict[key1])
            out.write(newline)
            
        elif key2 in aaDiffDict:
            if strainA in strains2:
                strains2.remove(strainA)
            if strainB in strains2:
                strains2.remove(strainB)
 
            newline = "%s\t%s\t%s\t%s\t%s\t%s\n" % \
                (lineLst[0], lineLst[1], lineLst[2], lineLst[3], lineLst[4], aaDiffDict[key2])
            out.write(newline)
 
    
 
    
#This is how I knew that all the strains of interest were found
#print(strains2)
#print(len(strains2))







aaDiffs.close()
hiDiffs.close()
out.close()