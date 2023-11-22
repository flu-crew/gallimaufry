#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take a fasta with sequences from one clade and apply 
a date filter (2018 to now)
Created by David E. Hufnagel on Aug 7, 2020
"""
import sys

inp = open(sys.argv[1])
out = open(sys.argv[2], "w")



isGood = False #Whether to write a sequence to the output 
for line in inp:
    if line.startswith(">"):
        lineLst = line.strip().strip(">").split("|")
        date = lineLst[-1]
        year = int(date.split("-")[0])

        if year >= 2018:
            out.write(line)
            isGood = True
        else:
            isGood = False
    else:
        if isGood and line != "\n":
            out.write(line)






inp.close()
out.close()
