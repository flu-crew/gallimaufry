#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take a list of names and create a 2-column file 
designed for coloration in fastTree.  This second column will often be the
clade 
Created by David E. Hufnagel on Aug 18, 2020
"""
import sys

inp = open(sys.argv[1])
out = open(sys.argv[2], "w")



for line in inp:
    lineLst = line.strip().split("|")
    print(lineLst[0])


inp.close()
out.close()