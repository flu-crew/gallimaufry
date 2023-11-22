#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script takes octoFLU results, a coded fasta file, and a text file 
for decoding and splits results into one decoded H1 fasta file and one 
decoded H3 fasta file
Created by David E. Hufnagel on Jul 13, 2020
"""
import sys

fasta = open(sys.argv[1])
octoResults = open(sys.argv[2])
decoder = open(sys.argv[3])
outH1 = open(sys.argv[4], "w")
outH3 = open(sys.argv[5], "w")


#Go through decoder and make a dict of key: codeName  val: fullName
decodeDict = {}
for line in decoder:
    lineLst = line.strip().split()
    codeName = lineLst[1]; fullName = lineLst[0]
    decodeDict[codeName] = fullName

#Go through octoResults and make a dict of key: codeName  val: HA subtype
octoDict = {}
for line in octoResults:
    lineLst = line.strip().split()
    codeName = lineLst[0]; haSub = lineLst[1]
    if haSub in ["H1","H3"]:
        octoDict[codeName] = haSub
    else:
        octoDict[codeName] = "NA"

#Go through fasta, switch out names, and output fastas in two files,
#  One for H1 and one for H3
for line in fasta:
    if line.startswith(">"):
        codeName = line.strip().strip(">")
        if codeName != "26":  #octoFLU skipped 26
            fullName = decodeDict[codeName]
            haSub = octoDict[codeName]
            if haSub == "H1":
                newline = ">%s\n" % (fullName)
                outH1.write(newline)
                toKeep = True
            elif haSub == "H3":
                newline = ">%s\n" % (fullName)
                outH3.write(newline)
                toKeep = True 
            else:
                haSub == "NA"
                toKeep = False  
    
    else:
        if toKeep:
            if haSub == "H1":
                outH1.write(line)
            elif haSub == "H3":
                outH3.write(line)




fasta.close()
octoResults.close()
decoder.close()
outH1.close()
outH3.close()

