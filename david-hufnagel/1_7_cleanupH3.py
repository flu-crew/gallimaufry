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
        if len(lineLst) != 7: #The format has the wrong number of fields
            if len(lineLst) == 2:
                strain = lineLst[0]; subtype = lineLst[1]; date = "1968"
                newline = ">huReference|%s|%s|swine|HKG||%s\n" % (strain, subtype, date)
            elif len(lineLst) == 3:
                source = lineLst[0]; strain = lineLst[1]; subtype = lineLst[2]
                date = strain.split("/")[-1]
                newline = ">%s|%s|%s|swine|USA||%s\n" % (source, strain, subtype, date)
            elif len(lineLst) == 4:   
                source = "huVaccine"; strain = lineLst[1]; subtype = lineLst[2]
                date = strain.split("/")[-1]
                newline = ">%s|%s|%s|swine|USA||%s\n" % (source, strain, subtype, date)
        else:
            source = lineLst[0]; strain = lineLst[1]; subtype = lineLst[2]
            host = lineLst[3]; clade = lineLst[4]; country = lineLst[5]
            date = lineLst[6]
            
            if clade in ["BRA","CHN","THA","KOR","CAN"]:
                country = clade; clade = ""
            
            newline = ">%s|%s|%s|%s|%s|%s|%s\n" % (source, strain, subtype, host, country, clade, date)
        out.write(newline)

    else:
        out.write(line)







inp.close()
out.close()