#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created by David E. Hufnagel on Thu Dec 10 15:43:00 2020
"""
import sys

inp = open(sys.argv[1])
out = open(sys.argv[2], "w")


for line in inp:
    if line.startswith(">"):
        newline = ">offlu-canada|" + line.strip(">").replace(" ", "_")
        out.write(newline)
    else:
        out.write(line)




inp.close()
out.close()