#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script takes as input names files entitled with N1 clade and generates a 
new file with defline=clade for all sequences.
Created by David E. Hufnagel on May  2, 2023
"""

import sys, os

#Identify input and output files
inp = open("combinedN1data_v4_clean_simp.fasta")
out = open("namesWgroups.txt", "w")
cladeFiles = []
for file in os.listdir():
    if "names" in file:
        cladeFiles.append(file)




#Go through inp and make a list of seqs present
toOutput = []
for line in inp:
    if line.startswith(">"):
        simpDef = line.strip().strip(">").replace("(","_").replace(")","_").replace("'","_").replace("|","_").replace("/","_")
        toOutput.append(simpDef)


#Go through names files and generate the output
cladeDict = {}
for file in cladeFiles:
    fd = open(file)
    clade = file.split("_")[0]
    
    for line in fd:
        simpDef = line.strip().replace("(","_").replace(")","_").replace("'","_").replace("|","_").replace("/","_")
        if simpDef.startswith("public"):
            simpDef = simpDef.replace("public","NEW_public")
        
        if simpDef in toOutput:
            newline = "%s=%s\n" % (simpDef, clade)
            out.write(newline)

    fd.close()





inp.close()
out.close()