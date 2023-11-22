#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take a file intended to be an annotation by clade
for figtree and puts clade information in the deflines so they match what's 
in the tree
Created by David E. Hufnagl on Jul 30, 2020
"""
import sys

inp = open(sys.argv[1])
out = open(sys.argv[2], "w")



for line in inp:
    lineLst = line.strip().split("\t")
    clade = lineLst[1]
    before = "|".join(lineLst[0].split("|")[:4])
    after = "|".join(lineLst[0].split("|")[4:])
    newline = "%s|%s|%s\t%s\n" % (before, clade, after, clade)
    out.write(newline)




inp.close()
out.close()
