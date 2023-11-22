#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to bring back dashes within dates instead of 
underscores.
Created by David E. Hufnagel on Wed Jan 13, 2021
"""
import sys

inp = open(sys.argv[1])
out = open(sys.argv[2], "w")


for line in inp:
    if line.startswith(">"):
        lineLst = line.strip().split("_")
        
        #extract date 
        last = lineLst[-1]; secLast = lineLst[-2]; thirdLast = lineLst[-3]
        if len(last) == 4: #just year
            most = "_".join(lineLst[:-1])
            date = last
        elif len(last) == 2:
            if len(secLast) == 4: #year and month
                most = "_".join(lineLst[:-2])
                date = "%s-%s" % (secLast, last)
            elif len(secLast) == 2 and len(thirdLast) == 4: #year, month, and day
                most = "_".join(lineLst[:-3])
                date = "%s-%s-%s" % (thirdLast, secLast, last)
            else:
                print("ERROR!")
                sys.exit()
        else:
            print("ERROR!")
            sys.exit()
        newline = "%s_%s\n" % (most, date)
        out.write(newline)
        
    else:
        out.write(line)
    







inp.close()
out.close()