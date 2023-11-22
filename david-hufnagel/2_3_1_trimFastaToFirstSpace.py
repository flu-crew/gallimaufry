#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take a fasta file and remove everything after the 
   last space.  Also replaces the other spaces with underscores to prevent
   future problems.
Created by David E. Hufnagel on Fri May 14 16:08:49 2021
"""
import sys

inp = open(sys.argv[1])
out = open(sys.argv[2], "w")



for line in inp:
    if line.startswith(">"):
        newline = "_".join(line.split(" ")[:-1]) + "\n"
        out.write(newline)
    else:
        out.write(line)











inp.close()
out.close()