#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to combine several fasta files and mark where
they came from.
Created by David E. Hufnagel on Tue Jun  10, 2021
"""
import sys


inpHI = open("gammaProjMergedData_all_noACC_pdmGamma_MN45fix.fna")
inp0616 = open("gammaSeqs06_16_v2.fna")
inp2021 = open("gammaSeqs20_21_clean.fna")
inpC1ref = open("c1Ref.fna")
inpC2ref = open("c2Ref.fasta")
inpC3ref = open("c3Ref.fasta")
out = open("allGammaDataSetsCombined.fna", "w")




def SaveIntoDict(key, val, dictx):
    if key in dictx:
        dictx[key].append(val)
    else:
        dictx[key] = [val,]

def ReadFasta(fd): #Go through input and store the file in a dict of key: defline   val: seq
    fastaDict = {}
    oldDef = ""; oldSeq = ""
    for line in fd:
        if line.startswith(">"):
            if oldSeq != "":
                SaveIntoDict(oldDef, oldSeq, fastaDict)
                oldDef = line.strip().strip(">")
                oldSeq = ""
            else:
                oldDef = line.strip().strip(">")
        else:
            oldSeq += line.strip()
    else:
        SaveIntoDict(oldDef, oldSeq, fastaDict)
        
    return(fastaDict)



dictHI = ReadFasta(inpHI)
dict0616 = ReadFasta(inp0616)
dict2021 = ReadFasta(inp2021)


for defline, seq in dictHI.items():
    newDef = ">HIseq|%s" % (defline)
    if len(seq) == 1: 
        newline = "%s\n%s\n" % (newDef, seq[0])
        out.write(newline)
    else:
        print("ERROR1")
        sys.exit()
    

for defline, seq in dict0616.items():
    newDef = ">data06-16|%s" % ("|".join(defline.split("|")[1:]))
    if len(seq) == 1: 
        newline = "%s\n%s\n" % (newDef, seq[0])
        out.write(newline)
    else:
        print("ERROR2")
        sys.exit()


for defline, seq in dict2021.items():
    newDef = ">data20-21|%s" % ("|".join(defline.split("|")[1:]))
    if len(seq) == 1: 
        newline = "%s\n%s\n" % (newDef, seq[0])
        out.write(newline)
    else:
        print("ERROR3")
        sys.exit()
    
        
for line in inpC1ref:
    if line.startswith(">"):
        newDef = ">C1_Ref|%s\n" % (line.strip().strip(">"))
        out.write(newDef)
    else:
        if line != "\n":
            out.write(line)
        

for line in inpC2ref:
    if line.startswith(">"):
        newDef = ">C2_Ref|%s\n" % (line.strip().strip(">"))
        out.write(newDef) 
    else:
        if line != "\n":
            out.write(line)
        

for line in inpC3ref:
    if line.startswith(">"):
        newDef = ">C3_Ref|%s\n" % (line.strip().strip(">"))
        out.write(newDef)  
    else:
        if line != "\n":
            out.write(line)







inpHI.close()
inp0616.close()
inp2021.close()
out.close()