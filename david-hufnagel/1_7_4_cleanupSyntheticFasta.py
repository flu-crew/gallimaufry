#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to reformat synthetic HA data
Created by David E. Hufnagel on Mon Dec 21, 2020
"""
import sys


inp = open(sys.argv[1])      #input fasta file
out = open(sys.argv[2], "w") #reformatted fasta file



for line in inp:
    if line.startswith(">"):
        lineLst = line.strip().strip(">").split("|")
        strain = lineLst[2]; subtype = lineLst[3]; country = lineLst[7]
        clade = lineLst[6]; date = lineLst[-1].strip("-")
        
        newline = ">syntheticIAV|%s|%s|swine|%s|%s|%s\n" % (strain, subtype, country, clade, date)
        out.write(newline)
        print(lineLst)
        print(newline)
        print()
    else:
        if line.strip() != "":
            out.write(line)
