#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take a fasta file of N1 sequences and adds a 
'source' to the start of the defline, removes empty lines, and changes 'Swine'
to 'swine'.
Created by David E. Hufnagel on Fri Sep  4, 2020
"""
import sys

inp = open(sys.argv[1])
out = open(sys.argv[2], "w")



for line in inp:
    if line.startswith(">"):
        newline = line.replace(">", ">publicIAV|").replace("Swine","swine")
        out.write(newline)
    else:
        if line.strip() != "":
            out.write(line)




inp.close()
out.close()
