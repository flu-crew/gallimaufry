#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to reformat dates for MEGAcc to make names match to 
YYYY-MM-DD format
Created by Dr. David E. Hufnagel on Oct 30, 2020
"""
import sys



inp = open(sys.argv[1])  # aquaNames.txt
out = open(sys.argv[2], "w")  # aquaNamesReformat.txt



for line in inp:
    lineLst = line.strip().split("_")
    oldDate = lineLst[-1]
    newDate = oldDate.replace("-","_")
    newLineLst = lineLst[:-1]; newLineLst.append(newDate)
    newline = "%s\n" % ("_".join(newLineLst))
    out.write(newline)




inp.close()
out.close()