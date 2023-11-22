#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to split the fasta file into smaller fasta files
by clade name.
Created by David E. Hufnagel on Tue Dec 22 16:11:51 2020
"""
import sys

inp = open(sys.argv[1])



def WriteUsingDict(key, line, dictx):
    name = "%s.fasta" % (key)
    if key in dictx:
        dictx[key].write(line)
    else:
        dictx[key] = open(name, "w")
        dictx[key].write(line)
        




#Process input to make and write into output files
outDict = {}
for line in inp:
    if line.startswith(">"):
        lineLst = line.strip().strip(">").split("|")
        clade = lineLst[5]
    WriteUsingDict(clade, line, outDict)
        
            
#Close output files
for val in outDict.values():
    val.close()
    







inp.close() 