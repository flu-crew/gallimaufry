#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to reformat Canada shipment HA data
Created by David E. Hufnagel on Mon Dec 21, 2020
"""
import sys


inp = open(sys.argv[1])      #input fasta file
out = open(sys.argv[2], "w") #reformatted fasta file



for line in inp:
    if line.startswith(">"):
        lineLst = line.strip().strip(">").split("|")
        strain = lineLst[2]
        subtype = lineLst[3]
        if len(lineLst) == 4:
            clade = ""; date = ""
        else:
            clade = lineLst[5]; date = lineLst[-1]
        
        newline = ">CAN-shipment|%s|%s|swine|CAN|%s|%s\n" % (strain, subtype, clade, date)
        out.write(newline)
    else:
        out.write(line)




inp.close()
out.close()