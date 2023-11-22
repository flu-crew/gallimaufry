#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take a main fasta of NA sequences and an associated
fasta of HA sequences and make a resulting pair file with the format:
strain name    NA clade    HA clade    date

Created by David E. Hufnagel  Nov 10, 2020
Updated on Nov 17, 2020 for 10 years data
"""
import sys

fasta = open(sys.argv[1])         #n1s10yrs_v4_lowerSwine_simp.fna
naCladesFd = open(sys.argv[2])    #namesWgroups.txt
cladeColorsFd = open(sys.argv[3]) #cladeColors2.txt
out = open(sys.argv[4], "w")      #pairData_10yr.txt



def ReformatDate(oldDate):
        slashes = oldDate.count("-")
        
        if slashes == 2:   
            oldDateLst = oldDate.split("-")
            year = oldDateLst[2]; month = oldDateLst[0]; day = oldDateLst[1]
            newDate = "%s-%s-%s" % (year, month, day)
        elif slashes == 1:
            oldDateLst = oldDate.split("-")
            year = oldDateLst[1]; month = oldDateLst[0]
            newDate = "%s-%s" % (year, month)
        else:
            newDate = oldDate
            
        return(newDate)




#Go through clade colors and make a dict of key: color  val: clade
cladeColorDict = {}
for line in cladeColorsFd:
    lineLst = line.strip().split("\t")
    color = lineLst[0]; clade = lineLst[1]
    cladeColorDict[color] = clade
    
    
#Go through na clades and make a dict of key: strain  val: naClade
cladeDict = {}
for line in naCladesFd:
    color = line.strip().split("=")[1]
    #change newBlack to black
    if color == "newBlack":
        color = "black"
    
    clade = cladeColorDict[color]
    strain = "A_swine_" + "_".join(line.strip().split("swine")[1].strip("_").split("Swine")[0].strip("_").split("_")[:-1])

    cladeDict[strain] = clade

#Go through fasta, collect all data, and generate the output 
for line in fasta:
    if line.startswith(">"):
        strain = "A_swine_" + "_".join(line.strip().split("swine")[1].strip("_").split("Swine")[0].strip("_").split("_")[:-1])
        haClade = line.split("Swine")[1].split("_")[2]
        
        #correct for problems created by IQTREE's replacement of special characters with underscores
        if not (haClade.startswith("1A") or haClade.startswith("1B") or haClade.startswith("1C")):
            haClade = line.split("Swine")[1].split("_")[3]
        date = "-".join(line.split("Swine")[1].strip("_").split("_")[2:]).strip()
        if "1A" in date:
            date = "-".join(date.split("-")[1:])
        
        if "like" in date:
            extra = "-" + date.split("-like-")[0] + "-like"
            date = date.split("like-")[1]
            haClade += extra
            
        if haClade.count("-") > 2:
            haClade = haClade.split("-09-14")[0]
        
            
        naClade = cladeDict[strain]        
        newDate = ReformatDate(date)
        
        newline = "%s\t%s\t%s\t%s\n" % (strain, naClade, haClade, newDate)
        out.write(newline)





fasta.close()
naCladesFd.close()
cladeColorsFd.close()
out.close()