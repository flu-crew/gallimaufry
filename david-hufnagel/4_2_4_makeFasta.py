#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 13:36:27 2023

@author: david.hufnagel
"""
import sys

inp = open("001_2.txt")
out = open("001_2.fna", "w")





#BODY
inp.readline()
for line in inp:
    lineLst = line.strip().split("\t")
    newlines = ">%s|%s|%s||%s\n%s\n" % (lineLst[1],lineLst[2],lineLst[4],lineLst[3],lineLst[-1])
    
    out.write(newlines)





inp.close()
out.close()