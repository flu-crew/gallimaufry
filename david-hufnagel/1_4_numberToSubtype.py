#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take Candian swine IAV data in files seperated
by HA subtype and write that subtype into the sequence names
Created by David E. Hufnagel on July 13, 2020
"""
import sys

h1Inp = open(sys.argv[1])
h3Inp = open(sys.argv[2])
outH1 = open(sys.argv[3], "w")
outH3 = open(sys.argv[4], "w")


for line in h1Inp:
    if line.startswith(">"):
        name = line.strip().strip(">")
        newName = name.split("__")[0] + "_H1"
        newline = ">%s\n" % (newName)
        outH1.write(newline)
    else:
        outH1.write(line)
        
for line in h3Inp:
    if line.startswith(">"):
        name = line.strip().strip(">")
        newName = name.split("__")[0] + "_H3"
        newline = ">%s\n" % (newName)
        outH3.write(newline)
    else:
        outH3.write(line)








h1Inp.close()
h3Inp.close()
outH1.close()
outH3.close()

