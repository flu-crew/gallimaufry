#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take a fasta file with fairly standard deflines
as input and add the state to the defline based on strain name.
Created by David E. Hufnagel on Mon Dec 14, 2020
"""
import sys

inp = open(sys.argv[1])
out = open(sys.argv[2], "w")



for line in inp:
    if line.startswith(">"):
        lineLst = line.strip().split("|")
        strain = lineLst[1]
        state = "_".join(strain.split("/")[2:-2])
        newLine = "%s|%s|%s|%s|%s|%s|%s|%s\n" % (lineLst[0], lineLst[1], lineLst[2], lineLst[3], lineLst[4], lineLst[5], state, lineLst[-1])
        out.write(newLine)
    else:
        out.write(line)









inp.close()
out.close() 