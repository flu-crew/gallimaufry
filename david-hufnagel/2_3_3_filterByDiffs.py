#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to filter a spreadsheet of aaDiff and antigenic
distance data by having below a certain level of aaDiff and above a certain
level of antigenic distance.
Created by David E. Hufnagel on Thu Apr 15 12:10:03 2021
"""
import sys

inp = open(sys.argv[1])         #gamma_compareAAdiffHIdiff.tab
out = open(sys.argv[2], "w")    #gamma_compareAAdiffHIdiff_outliers.tab
aaThresh = float(sys.argv[3])   #4  percent
antThresh = float(sys.argv[4])  #3  AU



title = inp.readline()
out.write(title)
for line in inp:
    lineLst = line.strip().split("\t")
    antDist = float(lineLst[4])
    
    if str(antDist) != "nan":
        aaDist = float(lineLst[5])
        
        if antDist > antThresh and aaDist < aaThresh:
            out.write(line)





inp.close()
out.close()