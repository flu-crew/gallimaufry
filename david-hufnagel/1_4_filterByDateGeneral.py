#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take a fasta with sequences from one clade and apply 
a date filter using a chosen date in the form: YYYY-MM-DD assuming we want all
sequences on or after a certain date.
Created by David E. Hufnagel on Aug 18, 2020
"""
import sys

inp = open(sys.argv[1])
out = open(sys.argv[2], "w")
dateThresh = sys.argv[3]      #YYYY-MM-DD

dateTlst = dateThresh.split("-")
yearT = int(dateTlst[0])
monthT = int(dateTlst[1])
dayT = int(dateTlst[2])





isGood = False #Whether to write a sequence to the output 
for line in inp:
    if line.startswith(">") and not "onsensus" in line:
        lineLst = line.strip().strip(">").split("|")
        date = lineLst[-1]
        dateLst = date.split("-")
        if len(dateLst) == 3:
            year = int(dateLst[0])
            month = int(dateLst[1])
            day = int(dateLst[2])
        elif len(dateLst) == 2:
            year = int(dateLst[0])
            month = int(dateLst[1])
            day = 1
        elif len(dateLst) == 1:
            year = int(dateLst[0])
            month = 1    #day and month are set to 1 when unknown so it leans towards inclusion of samples with less data metadata
            day = 1
        else:
            print("ERROR!")
            print(dateLst)
            sys.exit()
        
        if year > yearT or (year == yearT and month > monthT) or (year == yearT and month == monthT and day >= dayT):
            out.write(line)
            isGood = True
        else:
            isGood = False        
        
    else:
        if isGood and line != "\n":
            out.write(line)






inp.close()
out.close()
