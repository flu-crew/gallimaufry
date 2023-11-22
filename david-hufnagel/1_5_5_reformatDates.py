#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to reformat dates for tempEST to YYYY-MM-DD format
Created by David E. Hufnagel on Oct 20, 2020
"""
import sys

inp = open(sys.argv[1])
out = open(sys.argv[2], "w")



for line in inp:
    if line.startswith(">"):
        lineLst = line.strip().split("|")
        oldDate = lineLst[-1]
        slashes = oldDate.count("/")
        
        if slashes == 2:   
            oldDateLst = oldDate.split("/")
            year = oldDateLst[2]; month = oldDateLst[0]; day = oldDateLst[1]
            newDate = "%s-%s-%s" % (year, month, day)
        elif slashes == 1:
            oldDateLst = oldDate.split("/")
            year = oldDateLst[1]; month = oldDateLst[0]
            newDate = "%s-%s" % (year, month)
        else:
            newDate = oldDate
            
        first = "|".join(lineLst[:-1])
        newline = "%s|%s\n" % (first, newDate)
        out.write(newline)

    else:
        out.write(line)




inp.close()
inp.close()