#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
simply ensures that the proper format exists in the H3 OFFLU file
Created by David E. Hufnagel on Tue Dec 22 09:55:29 2020
"""
import sys

inp = open(sys.argv[1])      #semi-formatted fasta
out = open(sys.argv[2], "w") #fully formatted fasta



for line in inp:
    if line.startswith(">"):
        lineLst = line.strip().strip(">").split("|")
        source = lineLst[0].replace("huVac","huVaccine").\
            replace("offlu","offlu-vcm").replace("ref","huReference").\
                replace("vcm-vcm","vcm")
        strain = lineLst[1]; subtype = lineLst[2].replace("H1Nx","H1")
        host = lineLst[3]; clade = lineLst[4]
        country = lineLst[5].replace("Italy","ITA"); date = lineLst[6]
        
        if clade in ["BRA","CAN","CHL","JAP","KOR"]:
             country = clade; clade = ""
             
        
        newline = ">%s|%s|%s|%s|%s|%s|%s\n" % (source, strain, subtype, host, country, clade, date)
        out.write(newline)

    else:
        out.write(line)







inp.close()
out.close()