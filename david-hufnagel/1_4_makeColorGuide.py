#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to make a 2 column file of strain names and categories
which are converted to colors in FigTree
Created by David E. Hufnagel on Aug  4, 2020
"""
import sys
h1Fd = open("allH1data_finalAligned2.fna")
h3Fd = open("allH3data_finalAligned2.fna")
selectFd = open("selectedStrains.txt")
outH1 = open("cladeClassifications_v4_H1.txt", "w")
outH3 = open("cladeClassifications_v4_H3.txt", "w")



def ProcessFasta(fd, out):
    for line in fd:
        if line.startswith(">"):
            if not "consensus" in line:
                lineLst = line.strip().strip(">").split("|")
                source = lineLst[0]
                clade = lineLst[4]
                if source == "publicIAV":
                    group = clade
                    newline = "%s\t%s\n" % (line.strip().strip(">"), group)
                    out.write(newline)


#Process fasta files
ProcessFasta(h1Fd, outH1)
ProcessFasta(h3Fd, outH3)

#Process selected strains
for line in selectFd:
    lineLst = line.strip().split("\t")
    subtype = lineLst[0]; defline = lineLst[2]
    newline = "%s\tselect\n" % (defline)
    if subtype == "H1":
        outH1.write(newline)
    elif subtype == "H3":
        outH3.write(newline)
    else:
        print("ERROR!")
        sys.exit()






h1Fd.close()
h3Fd.close()
selectFd.close()
outH1.close()
outH3.close()