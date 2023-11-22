#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 10:38:14 2020

@author: david.hufnagel
"""


inp = open("chinaPaperGenome.fna")
out = open("chinaPaperGenome_M.fna", "w")


for line in inp:
    if line.startswith(">"):
        if "|MP" in line or "(MP)" in line or "gene=M1" in line or "gene=M2" in line:
            out.write(line)
            keep = True
        else:
            keep = False
    else:
        if keep:
            out.write(line)
        
                  
                  
                  
inp.close()
out.close()