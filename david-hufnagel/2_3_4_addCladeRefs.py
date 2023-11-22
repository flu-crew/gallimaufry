#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to add clade reference sequences to amino acid fasta
files for the purpose of building trees including these references with the 
goal of identifying the 3 gamma clades.
Created by David E. Hufnagel on Tue Jun  8 10:38:13 2021
"""
import sys




refs = open("cladeRefs.faa")
hiFasta = open("gammaProjMergedData_all_noACC_gamma_MN45fix_trim.faa")
oldFasta = open("../2_Gammas2006-2016/gammaSeqs06_16_v2_trim_311lenFilt.faa")
newFasta = open("../3_Gammas2020-2021/gammaSeqs20_21_clean_trim_311filt.faa")
hiOut = open("gammaProjMergedData_v2.faa", "w")
oldOut = open("../2_Gammas2006-2016/gammaSeqs06_16_v3.faa", "w")
newOut = open("../3_Gammas2020-2021/gammaSeqs20_21_v2.faa", "w")





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


def ProcessDict(fastaDict, out):
    #process input first
    for defline, seq in fastaDict.items():
        if not ("A02478571" in defline or "A01797415" in defline or "A01731653" in defline):
            newline = ">%s\n%s\n" % (defline, seq[0])
            out.write(newline)
        
    #then add refs
    newline = "%s%s\n" % (refDict2["C1"][0], refDict2["C1"][1][0])
    out.write(newline)

    newline = "%s%s\n" % (refDict2["C2"][0], refDict2["C2"][1][0])
    out.write(newline)

    newline = "%s%s\n" % (refDict2["C3"][0], refDict2["C3"][1][0])
    out.write(newline)
    
    
def ProcessDictAddSource(fastaDict, out):
    #process input first
    for defline, seq in fastaDict.items():
        if not ("A02478571" in defline or "A01797415" in defline or "A01731653" in defline):
            newline = ">publicIAV|%s\n%s\n" % (defline, seq[0])
            out.write(newline)
        
    #then add refs
    newline = "%s%s\n" % (refDict2["C1"][0], refDict2["C1"][1][0])
    out.write(newline)

    newline = "%s%s\n" % (refDict2["C2"][0], refDict2["C2"][1][0])
    out.write(newline)

    newline = "%s%s\n" % (refDict2["C3"][0], refDict2["C3"][1][0])
    out.write(newline)





#Go through refs and make a dict of key: cladeName  val: (defline, seq) where
#   defline was modified to include the provenance
refDict = ReadFasta(refs)
refDict2 = {}
for defline, seq in refDict.items():
    if "A02478571" in defline:
        newDef = ">C1_Ref|%s\n" % (defline)
        refDict2["C1"] = (newDef, seq)
    elif "A01797415" in defline:
        tempDef = "|".join(defline.split("|")[1:])
        newDef = ">C2_Ref|%s\n" % (tempDef)
        refDict2["C2"] = (newDef, seq)
    elif "A01731653" in defline:
        tempDef = "|".join(defline.split("|")[1:])
        newDef = ">C3_Ref|%s\n" % (tempDef)
        refDict2["C3"] = (newDef, seq)   
        

#Go through each fasta file, remove the current representation of clade
#   references where present and add the new ones to the appropriate output
#   file
hiDict = ReadFasta(hiFasta)
oldDict = ReadFasta(oldFasta)
newDict  = ReadFasta(newFasta)


ProcessDictAddSource(hiDict, hiOut)
ProcessDict(oldDict, oldOut)
ProcessDict(newDict, newOut)







refs.close(); hiFasta.close(); oldFasta.close(); newFasta.close()
hiOut.close(); oldOut.close(); newOut.close()