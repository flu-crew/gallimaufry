#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script uses names files to reclassify the N1.E.X strains in a nucleotide
fasta file only when present in an amino acid fasta file.

Created by David E. Hufnagel on Aug 31, 2023
Updated on Sep 8, 2023 to make combinedN1data_v5_newCladeNofilt.aln
"""
import sys

groupsFd = open("namesWgroups.txt")   #a file used for connecting deflines to clade information
inpFastaNuc = open("combinedN1data_v5.aln")
inpFastaAA = open("combinedN1data_v6_faa.aln")
out = open("combinedN1data_v5_newCladeAAfilt.aln", "w")
outNoFilt = open("combinedN1data_v5_newCladeNofilt.aln", "w")





def SaveIntoDict(key, val, dictx):
    if key in dictx:
        dictx[key].append(val)
    else:
        dictx[key] = [val,]


def ReadFasta(fd): #Go through inp and store the file in a dict of key: defline   val: seq
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


def GetClade(fileName):
    code = fileName.split("_")[0]
    if code == "aqua":
        clade = "N1.E.3"
    elif code == "asparagus":
        clade = "N1.E.3.3.1.4"
    elif code == "blueberry":
        clade = "N1.E.2.1"
    elif code == "eggplant":
        clade = "N1.E.2.2"
    elif code == "fern":
        clade = "N1.E.3.3.1.2"
    elif code == "grape":
        clade = "N1.E.1"
    elif code == "maroon":
        clade = "N1.E.3.1"
    elif code == "midnight":
        clade = "N1.E.3.3"
    elif code == "mocha":
        clade = "N1.E.2.5"
    elif code == "moss":
        clade = "N1.E.2"
    elif code == "n1a":
        clade = "N1.A"
    elif code == "n1e":
        clade = "N1.E"
    elif code == "ocean":
        clade = "N1.E.3.3.1.1"    
    elif code == "orchid":
        clade = "N1.E.2.3"
    elif code == "plum":
        clade = "N1.E.3.3.1.3"
    elif code == "salmon":
        clade = "N1.E.3.3.1"
    elif code == "sky":
        clade = "N1.E.2.4"
    elif code == "tangerine":
        clade = "N1.E.3.2"
    else:
        print("ERROR!")
        sys.exit()

    return(clade)






#Go through groups file and make a dict of key: simpDefline  val: clade
cladeDict = {}
for line in groupsFd:
    lineLst = line.strip().split("=")
    cladeID = lineLst[1]
    clade = GetClade(cladeID)
    cladeDict[lineLst[0]] = clade
    

#Go through aa fasta and make a goodLst
goodLst = []
for line in inpFastaAA:
    if line.startswith(">"):
        goodLst.append(line.strip().strip(">"))


#Go through nuc fasta, grab the new clade, and output if in the goodLst
inpDict = ReadFasta(inpFastaNuc)
for defline, seqs in inpDict.items():
    if len(seqs) > 1:
        print("ERROR!")
        sys.exit()
    else:
        seq = seqs[0]
        defLst = defline.strip().split("|")
        clade = defLst[-3]
        simpDef = defline.replace("|","_").replace("/","_").replace("'","_").replace("+","_").replace("(","_").replace(")","_")
        if simpDef in cladeDict:
            clade = cladeDict[simpDef]
        defLst[-3] = clade
        newDef = "|".join(defLst)
        newlines = ">%s\n%s\n" % (newDef, seq)
        outNoFilt.write(newlines)
        if defline in goodLst:
            out.write(newlines)












groupsFd.close()
inpFastaNuc.close()
inpFastaAA.close()
out.close()
outNoFilt.close()