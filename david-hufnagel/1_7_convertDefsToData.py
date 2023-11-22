#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take an OFFLU fasta from the 2021 February 
report and convert the deflines into data in a tabular format that can be
viewed in MS Excel for easy access with a broader audience.
Created by David E. Hufnagel on Wed Mar 31 20:20:11 2021
"""
import sys

inp = open(sys.argv[1])
out = open(sys.argv[2], "w")



title = "provenance\tHItest 2019\tHItest 2020 spring\tHItest 2020 fall\tHItest 2021 spring\tstrain\tsubtype\thost\tcountry\tclade\tdate\n"
out.write(title)
for line in inp:
    if line.startswith(">") and "onsensus" not in line:
        lineLst = line.strip().strip(">").split("|")
        
        cnt = 1
        for field in lineLst[1:5]:
            if field == "":
                lineLst[cnt] = "N"
            else:
                lineLst[cnt] = "Y"
            cnt += 1 
        
        newline = "%s\n" % ("\t".join(lineLst))
        out.write(newline)



inp.close()
out.close()