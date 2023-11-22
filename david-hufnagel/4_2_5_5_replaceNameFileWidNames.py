#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to replace names in a names file with IDs using a 
reference file where each line has this format: id      defline
Created by David E. Hufnagel on Aug 10, 2023

#modified to work with names files
"""
import sys

refs = open(sys.argv[1])       #The reference file with defline IDs
inpNames = open(sys.argv[2])   #The names fofn file (one line per names file name)





#Go through ref and make a dict of key: defline  val: id
nameChange = {}
for line in refs:
    lineLst = line.strip().split("\t")
    idName = lineLst[0]; defline = lineLst[1]
    nameChange[defline] = idName


#Go through each line in each names file, replace the defline with the idName, 
#   and output the result
for fileName in inpNames:
    fd = open(fileName.strip())
    outName = fileName.strip().replace(".txt",".id.txt")
    out = open(outName, "w")#A new names file with ID names
    
    for line in fd:
        newLine = line.replace(line.strip(), nameChange[line.strip()])
        out.write(newLine)
        
        
    fd.close()
    out.close()





refs.close()
inpNames.close()
