#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script uses names files to reclassify the N1.E.X strains in both a fasta
and a treefile. Note there are strains in the names files that are not in the
fasta and tree files because some more problematic sequences were removed
between the nucleotide trees used for classification and the amino acids used
for ancestral sequence generation

Created by David E. Hufnagel on Aug 26, 2023
"""
import sys

namesFd = open("names.txt")   #fofn of names files
inpFasta = open("combinedN1data_v6_faa.aln")
inpTree = open("combinedN1data_v6_faa.aln.nameFix.treefile")
outFasta = open("combinedN1data_v6_faa.n1Esplit.aln", "w")
outTree = open("combinedN1data_v6_faa.aln.nameFix.n1Esplit.treefile", "w")





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




#Go through inpFasta and make a dict of key: iqTreeDefline val: defline
iqTranslateDict = {}
for line in inpFasta:
    if line.startswith(">"):
        defline = line.strip().strip(">")
        iqTreeDef = defline.replace("|","_").replace("/","_").replace("'","_").replace("+","_").replace("(","_").replace(")","_")
        iqTranslateDict[iqTreeDef] = defline


#Go through names files, use iqTranslateDict to get defline and make a dict of 
#  key: defline   val: newClade where strains overlap
newCladeDict = {}
for line in namesFd:
    filename = line.strip()
    clade = GetClade(filename)
    
    fd = open(filename)
    for line in fd:
        if line.strip() in iqTranslateDict:
            defline = iqTranslateDict[line.strip()]
            newCladeDict[defline] = clade

    fd.close()


#Go through fasta again, use newCladeDict, insert new clades for N1.E.X 
#  strains, and output the result to outFasta. Also make a dict of 
#  key: defline  val: newDefline
newDeflineDict = {}
inpFasta.seek(0)
for line in inpFasta:
    if line.startswith(">"):
        defLst = line.strip().split("|")
        oldClade = defLst[-3]
        defline = line.strip().strip(">")
        if "N1.E" in oldClade:
            newClade = newCladeDict[defline]
            defLst[-3] = newClade
            newDef = ">%s\n" % ("|".join(defLst))
            outFasta.write(newDef)
            newDeflineDict[defline] = newDef.strip().strip(">")
        else:
            outFasta.write(line)
            newDeflineDict[defline] = defline
    else:
        outFasta.write(line)


#Go through inpTree and replace old deflines with new ones containing the new clades
for line in inpTree:
    isReplaced = False

    for oldDef, newDef in newDeflineDict.items():
        if oldDef in line and oldDef != newDef:
            line = line.replace(oldDef, newDef)
            isReplaced = True
    
    outTree.write(line)











namesFd.close()
inpFasta.close()
inpTree.close()
outFasta.close()
outTree.close()
