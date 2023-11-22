#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take a fasta file and a text file of deflines
and remove sequences with those deflines and keep all others
Created by David E. Hufnagel on Aug 21, 2020
"""
import sys

fasta = open(sys.argv[1])
badFd = open(sys.argv[2])
out = open(sys.argv[3], "w")



#Go through badFd and make a list of deflines to remove
badLst = []
for line in badFd:
    badLst.append(line.strip())

#Go through fasta and keep only sequences not in the badLst
isGood = True
for line in fasta:
    if line.startswith(">"):
        if line.strip().strip(">") in badLst:
            isGood = False
        else:
            isGood = True
            out.write(line)
    else:
        if isGood:
            out.write(line)

fasta.close()
badFd.close()
out.close()