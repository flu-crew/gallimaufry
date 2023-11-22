#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script simply adds a bit of text to the start of a defline followed by a "|"
Created day David E. Hufnagel on Mar 21, 2023
"""
import sys


inp = open(sys.argv[1])
out = open(sys.argv[2], "w")
text = sys.argv[3]





### BODY ###
for line in inp:
    if line.startswith(">"):
        new = ">" + text + "|"
        newline = line.replace(">",new)
        out.write(newline)
    else:
        out.write(line)






inp.close()
out.close()