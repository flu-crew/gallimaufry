#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script adds an empty category for the HA clade for deflines that start 
with "NEW" to make the number of fields match the deflines that start with "REF"
Created by David E. Hufnagel on May  9, 2023
"""
import sys

inp = open(sys.argv[1])
out = open(sys.argv[2], "w")





#BODY
for line in inp:
    if line.startswith(">NEW"):
        lineLst = line.strip().split("|")
        lineLst.insert(7,"")
        newline = "|".join(lineLst) + "\n"
        out.write(newline)
    else:
        out.write(line)







inp.close()
out.close()
