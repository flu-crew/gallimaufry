#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take a mostly raw fasta file with Canadian swine
IAV sequences having duplicate names and adds a number to the end to make 
them unique

Created by David E. Hufnagel on Jul 13, 2020
"""
import sys

inp = open(sys.argv[1])
out = open(sys.argv[2], "w")



def SaveIntoNumDict(key, dictX):
    if key not in dictX:
        dictX[key] = 1
    else:
        dictX[key] += 1



usedNames = {}  #key = name  val = cnt
for line in inp:
    if line.startswith(">"):
        name = line.strip()
        SaveIntoNumDict(name, usedNames)
        
        newline = "%s__%s\n" % (name, usedNames[name])
        out.write(newline)
    else:
        out.write(line)






inp.close()
out.close()

