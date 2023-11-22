#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take names files fasta files, extract the 
region-related information present in them, and output the information in 
a tabular format for processing in R like so:
strain    naClade    region.
Created by David E. Hufnagel on Apr 6, 2021
Modified on May 27, 2021 to use only US states
"""
import sys


inp = open(sys.argv[1])      #allN1s_v4.fna
out = open(sys.argv[2], "w") #allN1s_v4_stateData.tab




def SaveIntoCntDict(key, dictx):
    if key in dictx:
        dictx[key] += 1
    else:
        dictx[key] = 1
        
def GetRegion(cntry, strain):
    if cntry == "USA":
        region = strain.split("/")[2]
        if region in ["IL", "Ilinois", "Illinois"]:
            return("IL")
        elif region in ["IN", "Indiana"]:
            return("IN")
        elif region in ["MI", "Michigan"]:
            return("MI")
        elif region in ["MN", "Minneosta", "Minnesota", "Minnestoa", "Minnoosta"]:
            return("MN")
        elif region in ["MO", "Missouri"]:
            return("MO")
        elif region in ["NC", "North_Carolina", "North_Carollina"]:
            return("NC")
        elif region in ["OH", "Ohio"]:
            return("OH")
        elif region in ["SD", "SouthDakota", "South_Dakota"]:
            return("SD")
        elif region in ["IA", "Iowa"]:
            return("IA")
        elif region in ["Memphis", "TN", "Tennessee"]:
            return("TN")
        elif region in ["NE", "Nebraska"]:
            return("NE")
        elif region in ["Alabama"]:
            return("AL")
        elif region in ["Arizona"]:
            return("AZ")
        elif region in ["Arkansas"]:
            return("AR")
        elif region in ["California"]:
            return("CA")
        elif region in ["Colorado"]:
            return("CO")
        elif region in ["Florida"]:
            return("FL")
        elif region in ["Georgia"]:
            return("GA")
        elif region in ["Kansas"]:
            return("KS")
        elif region in ["Kentucky"]:
            return("KY")
        elif region in ["Maryland"]:
            return("MD")
        elif region in ["Mississippi"]:
            return("MS")
        elif region in ["North_Dakota"]:
            return("ND")
        elif region in ["Oklahoma"]:
            return("OK")
        elif region in ["OR"]:
            return("OR")
        elif region in ["Pennsylvania"]:
            return("PA")
        elif region in ["South_Carolina"]:
            return("SC")
        elif region in ["Texas"]:
            return("TX")
        elif region in ["United_States", "USA"]:
            return("NA")
        elif region in ["Utah"]:
            return("UT")
        elif region in ["Virginia"]:
            return("VA")
        elif region in ["Wisconsin"]:
            return("WI")
        elif region in ["Jamesburg"]:
            return("NJ")
        else:
            print(region)
    else:
        return("NA") #Costa Rica, Guatemala, and Cuba
        
        
        
        
for line in inp:
    if line.startswith(">"):
        lineLst = line.strip().split("|")
        strain = lineLst[1]; cntry = lineLst[4]; clade = lineLst[5]
        region = GetRegion(cntry, strain)
        if region != "NA":
            newline = "%s\t%s\t%s\n" % (strain, clade, region)
            out.write(newline)




inp.close()
out.close()
