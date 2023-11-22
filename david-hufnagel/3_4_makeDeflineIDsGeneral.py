#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take a fasta as input, convert the deflines to 
unique IDs, and create a 2-column tabular reference file with the format:
ID    wholeDefline
The purpose of this script is to create a fasta that can easily be handled
by sensitive software and then the output could use the reference file to
restore the original names.

Created by David E. Hufnagel on May 18, 2022
"""
import sys

inp = open(sys.argv[1])
outFasta = open(sys.argv[2], "w")
outRef = open(sys.argv[3], "w")





cnt = 1
for line in inp:
    if line.startswith(">"):
        #gather data
        defline = line.strip().strip(">")
        code = "ID" + str(cnt).zfill(10)
        
        #output fasta
        newDef = ">%s\n" % (code)
        outFasta.write(newDef)
        
        #output ref
        refLine = "%s\t%s\n" % (code, defline)
        outRef.write(refLine)
        
        cnt += 1
    else:
        outFasta.write(line)

    
    












inp.close()
outFasta.close()
outRef.close()