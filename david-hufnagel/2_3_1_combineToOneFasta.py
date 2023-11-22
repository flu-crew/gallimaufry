#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script combines the sequences that I found on genbank with the one I
could not and also completes the reformatting.
Created by David E. Hufnagel on Mon Apr 12 15:44:02 2021
"""
import sys

oneFasta = open(sys.argv[1])
manyFasta = open(sys.argv[2])
out = open(sys.argv[3], "w")



for line in oneFasta:
    if line.startswith(">"):
        out.write(line.replace("|||||","|").replace("CVV|",""))
    else:
        if line != "\n":
            out.write(line)
        
        
for line in manyFasta:
    if line.startswith(">"):
        lineLst = line.strip().split("|"); strain = lineLst[0]
        host = lineLst[1]; country = lineLst[2]; date = lineLst[3]
        if date == "NON--":
            date = ""
        date = date.strip("-")
        
        newline = "%s||%s|%s||%s\n" % (strain, host, country, date)
        out.write(newline)
    else:
        if line != "\n":
            out.write(line)





oneFasta
manyFasta
out
