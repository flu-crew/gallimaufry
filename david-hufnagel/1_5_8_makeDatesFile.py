#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take a fasta file and make a 2-col output with 
the format:  defline   date
Created by David E. Hufnagel on Nov 12, 2020
"""
import sys

inp = open(sys.argv[1])
out = open(sys.argv[2], "w")



for line in inp:
    if line.startswith(">"):
        defline = line.strip().strip(">").replace("/","_").replace("|","_")
        date = line.strip().split("|")[-1]
        newline = "%s\t%s\n" % (defline, date)
        out.write(newline)




inp.close()
out.close()