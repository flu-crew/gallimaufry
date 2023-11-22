#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take a fasta file with deflines delimited by "|"
and and make a 2 column file of the whole defline first and a specific column
second.  The original use for this script is preparing a data file for
BEAUTi to import HA clade information

Created by David E. Hufnagel on Tue May  4 16:31:44 2021
"""
import sys

inp = open(sys.argv[1])      #input file
out = open(sys.argv[2], "w") #output file
col = int(sys.argv[3])       #the column of the information to be extracted.  Example: if the defline structure is "public|strain|HAclade|date", "3" would be this parameter if you want to extract the HAclade 
col -= 1                     #adjust for python starting the count at 0



for line in inp:
    if line.startswith(">"):
        lineLst = line.strip().split("|")
        defline = line.strip().strip(">")
        dataPt = lineLst[col]
        newline = "%s\t%s\n" % (defline, dataPt)
        out.write(newline)




inp.close()
out.close()