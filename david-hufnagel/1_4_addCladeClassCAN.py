#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to add clade classifications back to Canadian sequences
that were removed previously

Created by David E. Hufnagel on Aug 13, 2020
"""
import sys
inp = open(sys.argv[1])
classFd = open(sys.argv[2])
out = open(sys.argv[3], "w")



#Go through classification and store clade info in a dict of key: defline val: clade
classDict = {}
for line in classFd:
    lineLst = line.strip().split("\t")
    defLst = lineLst[0].split("|")
    newDef = "%s|%s" % ("|".join(defLst[:4]), "|".join(defLst[5:]))
    classDict[newDef] = lineLst[1]

#Go through input file, add in clade info where absent, and output
for line in inp:
    if line.startswith(">"):
        lineLst = line.strip().strip(">").split("|")
        clade = lineLst[4]
        if clade == "unknown":
            newDef = "%s|%s" % ("|".join(lineLst[:4]), "|".join(lineLst[5:]))
            print(lineLst)
            print(newDef)
            print(clade)
            clade = classDict[newDef]
            sys.exit()
            print()


#####Need to remove clade from deflines in both files to connect the two files 


inp.close()
classFd.close()
out.close()