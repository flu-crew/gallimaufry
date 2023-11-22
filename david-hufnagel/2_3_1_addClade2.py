#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to filter by and add information about clades to our
   1A distance fasta file.
Created by David E. Hufnagel on Mon Apr 12 16:41:46 2021
Modified on May 18, 2021 to use an octuflu input for clades and keep only
   pandemic and gamma clades.
"""
import sys


fasta = open(sys.argv[1])          #gammaProjMergedData_all_noACC.fna 
octoFd = open(sys.argv[2])         #gammaProjMergedData_all_noACC.fna_Final_Output.txt
out = open(sys.argv[3], "w")       #gammaProjMergedData_all_noACC_pdmGamma.fna
outUnfilt = open(sys.argv[4], "w") #gammaProjMergedData_all_noACC_noFilt.fna



#Go through octoFd and make a dict of key: strain  val: (subtype, clade).  
cladeDict = {}
for line in octoFd:
    lineLst = line.strip().split("\t")
    strain = "_".join(lineLst[0].split("_")[:-3]).upper()
    clade = lineLst[3].replace("-vaccine","")
    subtype = "H1"
    cladeDict[strain.upper()] = (subtype, clade)


#Go through fasta and make a dict of key: strain  val: (defline, seq)
fastaDict = {}
oldStrain = ""; oldDef = ""; oldSeq = ""
for line in fasta:
    if line.startswith(">"):
        if oldStrain != "":
            fastaDict[oldStrain.upper()] = (oldDef, oldSeq)
            oldDef = line.strip().strip(">")
            oldStrain = oldDef.split("|")[0]
            oldSeq = ""
        else:
            oldDef = line.strip().strip(">")
            oldStrain = oldDef.split("|")[0]
    else:
        oldSeq += line.strip()
else:
    fastaDict[oldStrain.upper()] = (oldDef, oldSeq)
    

#Go through fastaDict and output lines that are in the octoDict along with
#   subtype and clade data
for strain, val in fastaDict.items():        
    if strain.upper() in cladeDict:
        subtype = cladeDict[strain.upper()][0]
        clade = cladeDict[strain.upper()][1]
        defline = val[0]
        defLst = defline.split("|")
        defLst.insert(1, subtype)
        defLst.insert(4, clade)
        
        newDef = ">" + "|".join(defLst) + "\n"
        seq = val[1] + "\n"
        
        if clade in ["1A.3.3.3", "1A.3.3.2"]:
            out.write(newDef)
            out.write(seq)

        outUnfilt.write(newDef)
        outUnfilt.write(seq)
        






fasta.close()
octoFd.close()
out.close()
outUnfilt.close()