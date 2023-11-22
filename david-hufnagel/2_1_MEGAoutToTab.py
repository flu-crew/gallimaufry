#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to make it easier to copy values from a MEGA between
clade patristic distance output into an excel file by converting it to tabular
format.
Created by David E. Hufnagel on Wed Jan 13, 2021
"""
import sys

inp = open(sys.argv[1])
out = open(sys.argv[2], "w")


#skip to start of # lines 
inp.readline()
for line in inp:
    if "#" in line:
        break

#skip to start of data lines, extract data, and output it
cnt = 0
for line in inp:
    if not ("#" in line or line.strip() == ""):
        if cnt > 1:
            dataChunk = line[4:].strip()
            dataLst = dataChunk.split()
            newline = "%s\n" % ("\t".join(dataLst))
            out.write(newline)
        cnt += 1





inp.close()
out.close()
