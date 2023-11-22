#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take an NA fasta file with a specific set of 
sequences and an HA fasta file with a great number of sequences and produce an 
HA fasta with with only the sequences that are associated with the
provided NA sequences.
Created By David E. Hufnagel on Thu Nov 19, 2020
"""
import sys

naInp = open(sys.argv[1])      #n1dataSep_v5_reformat.fna
haInp = open(sys.argv[2])      #HA-101-2-years.fna
haInpIRD = open(sys.argv[3])   #has_ird_2yrs_formated.fna 
out = open(sys.argv[4], "w") #HA-101-2-years_n1PairOnly.fna
#outNA = open(sys.argv[5], "w") #n1dataSep_v5_reformat_n1PairOnly.fna



#Go through haInp and make a dict of key: strain  val: (defline, seq)
lastDef = ""; lastSeq = ""; haDict = {}
for line in haInp:
    if line.startswith(">"):
        if lastSeq != "":
            strain = lastDef.split("|")[1]
            haDict[strain] = (lastDef, lastSeq)
        lastDef = line.strip().strip("\n")
        lastSeq = ""
    else:
        lastSeq += line.strip()
else:
    strain = lastDef.split("|")[1]
    haDict[strain] = (lastDef, lastSeq)
    

#Go though haInpIRD, add ha data to the haDict with a preference towards IRD data
lastDef = ""; lastSeq = ""
for line in haInpIRD:
    if line.startswith(">"):
        if lastSeq != "":
            strain = lastDef.split("|")[1]
            if strain not in haDict:
                print(strain)
            haDict[strain] = (lastDef, lastSeq)
        lastDef = line.strip().strip("\n")
        lastSeq = ""
    else:
        lastSeq += line.strip()
else:
    strain = lastDef.split("|")[1]
    if strain not in haDict:
        print(strain)
    haDict[strain] = (lastDef, lastSeq)
    


#Go through naInp, collect and reformat related ha data, and output ha data
for line in naInp:
    if line.startswith(">"):
        strain = line.split("|")[1]
        haData = haDict[strain]
        newlines = "%s\n%s\n" % (haData[0], haData[1])
        out.write(newlines)





naInp.close()   
haInp.close()
haInpIRD.close()
out.close()
#outNA.close()