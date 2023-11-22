#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take a main fasta of NA sequences and an associated
fasta of HA sequences and make a resulting pair file with the format:
strain name    NA clade    HA clade    date

Created by David E. Hufnagel  Nov 10, 2020
Updated on March 23, 2021 to use all years data
"""
import sys

fasta = open(sys.argv[1])         #allN1s_v3_aligned_reformat_noMixed_simp.fna
naCladesFd = open(sys.argv[2])    #namesWgroups.txt
cladeColorsFd = open(sys.argv[3]) #cladeColors.txt
out = open(sys.argv[4], "w")      #pairData_Ayr.txt




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
    strain = "A_Swine_" + "_".join(line.strip().split("Swine")[1].strip("_").split("_")[:-1])

    cladeDict[strain] = clade


#Go through fasta, collect all data, and generate the output 
for line in fasta:
    if line.startswith(">"):
        strain = "A_Swine_" + "_".join(line.strip().split("Swine")[1].strip("_").split("_")[:-1])
        haClade = "_".join(line.strip().split("Swine")[2].strip("_").split("_")[1:-1])#"_".join(line.split("Swine")[2].split("_")[2:-1]).replace("Rica_","")
        if "Rica" in haClade:
            haClade = haClade[5:]
        date = line.split("Swine")[2].strip("_").split("_")[-1].strip()       
        naClade = cladeDict[strain]        

        
        newline = "%s\t%s\t%s\t%s\n" % (strain, naClade, haClade, date)
        out.write(newline)





fasta.close()
naCladesFd.close()
cladeColorsFd.close()
out.close()