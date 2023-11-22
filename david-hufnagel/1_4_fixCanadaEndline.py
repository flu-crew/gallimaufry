#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take a fasta file of Canadian swine IAV's and 
fix where endlines have been omitted during concatenation in UNIX.  Also 
removes empty lines.
results in octoFLU.
Created by David E. Hufnagel on Jul 13, 2020
"""
import sys

inp = open(sys.argv[1])
out = open(sys.argv[2], "w")


usedNames = []
for line in inp:
    if not line.startswith(">"):
        newline = ""
        if line != "\n":
            for char in line:
                if char == ">":
                    newline += "\n"
                    newline += char
                else:
                    newline += char
            out.write(newline)
        
    else:
        out.write(line)



inp.close()
out.close()