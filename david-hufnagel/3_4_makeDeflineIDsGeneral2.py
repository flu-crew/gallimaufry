#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take a fasta as input, convert the deflines to 
unique IDs, and create a 2-column tabular reference file with the format:
ID    wholeDefline
The purpose of this script is to create a fasta that can easily be handled
by sensitive software and then the output could use the reference file to
restore the original names.

Created by David E. Hufnagel on May 18, 2022
Updated on Aug 25, 2023 to also replace the names in the namesWgroups.txt
   file for MEGAcc
"""
import sys

inp = open(sys.argv[1])
outFasta = open(sys.argv[2], "w")
outRef = open(sys.argv[3], "w")
inpGroups = open(sys.argv[4])
outGroups = open(sys.argv[5], "w")





#Go through the input fasta, make an ID for each defline, output the fasta with
#  IDs as well as the ID reference file. Also store the ID in a dict of
#  key: defline   val: ID
idDict = {}
cnt = 1
for line in inp:
    if line.startswith(">"):
        #gather data
        defline = line.strip().strip(">")
        code = str(cnt).zfill(10)
        
        #output fasta
        newDef = ">%s\n" % (code)
        outFasta.write(newDef)
        
        #output ref
        refLine = "%s\t%s\n" % (code, defline)
        outRef.write(refLine)
        idDict[defline] = code
        
        cnt += 1
    else:
        outFasta.write(line)

    
#Go through the input names file, replace deflines with IDs using idDict,
#  and output the result
for line in inpGroups:
    defline = line.strip().strip(">").split("=")[0]
    code = idDict[defline]
    
    newline = line.replace(defline, code)
    outGroups.write(newline)









inp.close()
outFasta.close()
outRef.close()
inpGroups.close()
outGroups.close()