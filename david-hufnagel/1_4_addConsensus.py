#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take a big fasta file for H1 and another for H3 and 
add consensus sequences to each file.
Created by David E. Hufnagel on Jul 30, 2020
"""
import sys

bigH1Fd = open(sys.argv[1])
bigH3Fd = open(sys.argv[2])
consensusH1Fd = open(sys.argv[3]) #many consensus files in fofn format for H1
consensusH3Fd = open(sys.argv[4]) #many consensus files in fofn format for H1
outH1 = open(sys.argv[5], "w")
outH3 = open(sys.argv[6], "w")



#pipe big fastas directly to the outputs
for line in bigH1Fd:
    outH1.write(line)
for line in bigH3Fd:
    outH3.write(line)

#Go through consensus files, make deflines that are informative, and pipe them 
#  to the outputs 
for line in consensusH1Fd:
    fileName = line.strip()
    fd = open(fileName)
    for line in fd:
        if line.startswith(">"):
            clade = fileName.split("Only_consensus")[0]
            name = "%s_consensus" % (clade)
            newline = ">%s\n" % (name)
            outH1.write(newline)
        else:
            outH1.write(line)
            
    fd.close()
            
for line in consensusH3Fd:
    fileName = line.strip()
    fd = open(fileName)
    for line in fd:
        if line.startswith(">"):
            clade = fileName.split("Only_consensus")[0]
            name = "%s_consensus" % (clade)
            newline = ">%s\n" % (name)
            outH3.write(newline)
        else:
            outH3.write(line)
            
    fd.close()






bigH1Fd.close()
bigH3Fd.close()
consensusH1Fd.close()
consensusH3Fd.close()
outH1.close()
outH3.close()
