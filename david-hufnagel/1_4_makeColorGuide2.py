#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to make a 2 column file of strain names and categories
which are converted to colors in FigTree
Created by David E. Hufnagel on Aug  20, 2020
"""
import sys
inp = open(sys.argv[1])
out = open(sys.argv[2], "w")



for line in inp:
    if line.startswith(">"):
        if "onsensus" not in line:
            lineLst = line.strip().strip(">").split("|")
            source = lineLst[0]
            clade = lineLst[4]
            if source in ["publicIAV", "offlu", "prevTest", "forHI"]:
                newline = "%s\t%s\n" % (line.strip().strip(">"), clade)
                out.write(newline)



inp.close()
out.close()