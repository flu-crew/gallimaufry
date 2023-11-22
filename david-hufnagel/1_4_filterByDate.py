#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take a fasta with many global sequences and apply a
date filter for the USA (January 2020-June 20) and a separate filter for 
outside the USA (2016-now)
Created by David E. Hufnagel on Jul 28, 2020
"""
import sys

inp = open(sys.argv[1])
out = open(sys.argv[2], "w")



isGood = False #Whether to write a sequence to the output 
for line in inp:
    if line.startswith(">"):
        lineLst = line.strip().strip(">").split("|")
        source = lineLst[0]
        if source == "publicIAV":
            country = lineLst[4]
            date = lineLst[5]
            if country == "USA":
                year = int(date.split("-")[0])
                month = int(date.split("-")[1])
                day = int(date.split("-")[2])

                if year in [20,2020] and month <= 6:
                    #reformat date
                    if year == 20:
                        year = 2020
                    newDate = "%s-%s-%s" % (year, str(month).zfill(2), str(day).zfill(2)) #standardize format
                    newline = "%s|%s\n" % ("|".join(line.split("|")[:-1]), newDate)
                    out.write(newline)
                    isGood = True
                else:
                    isGood = False
            else:
                year = int(date.split("-")[0])
                month = int(date.split("-")[1])
                day = int(date.split("-")[2])

                if year >= 2016:
                    newline = "%s|%s\n" % ("|".join(line.split("|")[:-1]), date)
                    out.write(newline)
                    isGood = True
                else:
                    isGood = False
        else:
            isGood = False
    else:
        if isGood and line != "\n":
            out.write(line)


            








inp.close()
out.close()
