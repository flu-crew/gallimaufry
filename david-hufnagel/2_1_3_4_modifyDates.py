#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modify dates to ensure that two "/" symbols are always used and the resulting 
structure is "MM/DD/YYYY".  Where data is not available data is added for 
plotting sake.
Created by David E. Hufnagel on Mon May 17 14:36:07 2021
"""
import sys


inp = open(sys.argv[1])      #strainMetaData_v2.txt
out = open(sys.argv[2], "w") #strainMetaData_v2_dateMod.txt


out.write(inp.readline())
for line in inp:
    lineLst = line.split("\t")
    date = lineLst[2]
    dateLst = date.split("/")
    if len(dateLst) == 1:
        newDate = "06/15/%s" % (dateLst[0])
    elif len(dateLst) == 2:
        newDate = "%s/15/%s" % (dateLst[0], dateLst[1])
    elif len(dateLst) == 3:
        newDate = date
    else:
        print("ERROR!")
        sys.exit()

    lineLst[2] = newDate
    newLine = "\t".join(lineLst)
    out.write(newLine)



inp.close()
out.close()