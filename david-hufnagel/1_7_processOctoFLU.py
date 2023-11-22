#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is designed to take a fasta file and it's octoFLU output file 
and keep a certain sequences
Created by David E. Hufnagel on Sun Dec 20 14:04:33 2020
"""
import sys

fasta = open(sys.argv[1])       #input fasta file with all sequences
octoResults = open(sys.argv[2]) #octoFLU results from the above fasta file
field = int(sys.argv[3])        #a integer (2-4) of the field to match (count starts at 1)
match = sys.argv[4]             #what to match (exact match or 'NA' or 'HA')
out = open(sys.argv[5], "w")    #output fasta file with only desired sequences



#Go through octoResults and process field and match to form a goodLst
goodLst = []
for line in octoResults:
    lineLst = line.strip().split()
    toMatch = lineLst[field-1]
    if match == "HA":
        if toMatch[0] == "H":
            goodLst.append(lineLst[0])
    elif match == "NA":
        if toMatch[0] == "N":
            goodLst.append(lineLst[0])
    else:
        if toMatch == match:
            goodLst.append(lineLst[0])


#Use the goodLst to output desired fasta lines using smof grep
currDefline = ""
for line in fasta:
    if line.startswith(">"):
        currDefline = line.strip().strip(">").replace(" ","_").replace("/","_").replace("|","_")
        print(currDefline)
        if currDefline in goodLst:
            out.write(line.replace(" ","_"))
    else:
        if currDefline in goodLst:
            out.write(line)





fasta.close()
octoResults.close()
out.close()


