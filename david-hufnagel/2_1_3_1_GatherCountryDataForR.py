#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take names files fasta files, extract the 
region-related information present in them, and output the information in 
a tabular format for processing in R like so:
strain    naClade    region.
Created by David E. Hufnagel on Apr 6, 2021
Modified on May 27 to use only countries
"""
import sys


inp = open(sys.argv[1])      #allN1s_v4.fna
out = open(sys.argv[2], "w") #allN1s_v4_cntryData.tab




def SaveIntoCntDict(key, dictx):
    if key in dictx:
        dictx[key] += 1
    else:
        dictx[key] = 1
        
def GetRegion(cntry, strain):
    if cntry == "USA":
        return("USA")
    elif cntry == "Mexico":
        return("MEX")
    elif cntry == "Canada":
        return("CAN")
    elif cntry == "Costa_Rica":
        return("CRI")
    elif cntry == "Cuba":
        return("CUB")
    elif cntry == "Guatemala":
        return("GTM")
    else:
        print("ERROR!")
        sys.exit()
        
        
        
        
for line in inp:
    if line.startswith(">"):
        lineLst = line.strip().split("|")
        strain = lineLst[1]; cntry = lineLst[4]; clade = lineLst[5]
        region = GetRegion(cntry, strain)
        newline = "%s\t%s\t%s\n" % (strain, clade, region)
        out.write(newline)




inp.close()
out.close()
