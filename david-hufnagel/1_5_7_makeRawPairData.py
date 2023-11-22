#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take a main fasta of NA sequences and an associated
fasta of HA sequences and make a resulting pair file with the format:
strain name    NA clade    HA clade    date

Created by David E. Hufnagel  Nov 10, 2020
"""
import sys

fasta = open(sys.argv[1])         #n1dataSep_v4_noCons_lenFilt.fna
naCladesFd = open(sys.argv[2])    #namesWgroups.txt
cladeColorsFd = open(sys.argv[3]) #cladeColors.txt
out = open(sys.argv[4], "w")      #pairData_2yr.txt



#Go through clade colors and make a dict of key: color  val: clade
cladeColorDict = {}
for line in cladeColorsFd:
    lineLst = line.strip().split("\t")
    color = lineLst[0]; clade = lineLst[1]
    cladeColorDict[color] = clade
    
    
#Go through na clades and make a dict of key: strain  val: naClade
cladeDict = {}
for line in naCladesFd:
    color = line.strip().split("=")[1]
    #change newBlack to black
    if color == "newBlack":
        color = "black"
    
    clade = cladeColorDict[color]
    strain = "A/swine/" + "/".join(line.strip().split("swine")[1].strip("_").split("_")[:-1])
    if strain.count("/") >= 5:
        strain = strain.replace("OH/18/7963", "OH_18_7963").replace("SouthDakota","South_Dakota").replace("/Dakota","_Dakota").replace("/Carolina","_Carolina").replace("/Carollina", "_Carolina")

    cladeDict[strain] = clade

#Go through fasta, collect all data, and generate the output 
for line in fasta:
    if line.startswith(">"):
        lineLst = line.strip().strip(">").split("|")
        strain = lineLst[1]; haClade = lineLst[5]
        naClade = cladeDict[strain]
        newline = "%s\t%s\t%s\t%s\n" % (strain, naClade, haClade, lineLst[-1])
        out.write(newline)





fasta.close()
naCladesFd.close()
cladeColorsFd.close()
out.close()