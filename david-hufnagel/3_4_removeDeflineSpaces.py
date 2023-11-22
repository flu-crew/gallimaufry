#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to simply remove spaces from a fasta's deflines
Created on May 17, 2022 by David E. Hufnagel
"""
import sys
inp = open(sys.argv[1])
out = open(sys.argv[2], "w")



for line in inp:
    if line.startswith(">"):
        newline = line.replace(" ","_")
        out.write(newline)
    else:
        out.write(line)






inp.close()
out.close()