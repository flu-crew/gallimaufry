#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take a big fasta file and 
add consensus sequences to each file.
Created by David E. Hufnagel on Sep 10, 2020
"""
import sys

fastaFd = open(sys.argv[1])
consensusFofn = open(sys.argv[2]) #many consensus files in fofn format
out = open(sys.argv[3], "w")



def GetClade(color):
    if color == "black":
        return("Other")
    elif color == "blueberry":
        return("1B.1")
    elif color == "clover":
        return("1A.2.2")
    elif color == "maraschino":
        return("1A.1")
    elif color == "mocha":
        return("1A.3")
    elif color == "tangerine":
        return("1A.2.1")
    else:
        print("ERROR!")
        sys.exit()






#pipe fasta directly to the output
for line in fastaFd:
    out.write(line)

#Go through consensus files, make deflines that are informative, and pipe them 
#  to the outputs
for line in consensusFofn:
    fileName = line.strip()
    fd = open(fileName)
    for line in fd:
        if line.startswith(">"):
            color = fileName.split("_cons")[0]
            clade = GetClade(color)
            name = "%s_consensus" % (clade)
            newline = ">%s\n" % (name)
            out.write(newline)
        else:
            out.write(line)
            
    fd.close()





fastaFd.close()
consensusFofn.close()
out.close()
