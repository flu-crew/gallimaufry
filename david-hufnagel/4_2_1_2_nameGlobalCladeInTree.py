#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to learn global N1 clade designations based on name
files and use that information to annotate trees with deflines updated with clade
Created by David E. Hufnagel on Wed AFeb 1, 2023
"""
import sys, os

inpTree = open("combinedN1s.aln_fix.tre")
inpFasta = open("combinedN1s.fna")
outTree = open("combinedN1s.aln_fix_cladeFill.tre", "w")
outFasta = open("combinedN1s_cladeFill.fna", "w")





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






#Go through names files and assign clades to deflines stored in a dict of 
#  key: defline, val: clade and a dict of key: inpDefline  val: outDefline
directory = '/Users/david.hufnagel/Documents/1_Research/4_2023/2_N1diversity/1_WorldwideN1Phylogeny/2_nameGlobal'
cladeDict = {}; outDict = {}
for fileName in os.listdir(directory):
    filePath = os.path.join(directory, fileName)
    if os.path.isfile(filePath) and fileName.startswith("names"):
        fd = open(filePath)
        for line in fd:
            clade = fileName.split("_")[1].split(".txt")[0]
            oldDef = line.strip()
            lineLst = oldDef.split("|")
            if lineLst[5] == "": #global
                lineLst[5] = clade
                lineLst[0] = "publicGlobal"
            else:
                lineLst[0] = "publicNAmer"
            newDef = "|".join(lineLst)
            cladeDict[oldDef] = clade
            outDict[oldDef] = newDef
        
        fd.close()


#Go through inpFasta and  make a dict of key: inpDefline  val: outDefline and 
#  output to outFasta
inpFastaDict = ReadFasta(inpFasta)
for oldDef, seqs in inpFastaDict.items():
    if len(seqs) != 1:
        print("ERROR1!")
        sys.exit()
    else:
        seq = seqs[0]
        newDef = outDict[oldDef]
        newlines = ">%s\n%s\n" % (newDef, seq)
        outFasta.write(newlines)


#Go through inpTree, replace the deflines with ones that include clade
#  designations and output to outTree
treeLst = inpTree.readlines()
if len(treeLst) == 1:
    treeStr = treeLst[0]
    for oldDef,newDef in outDict.items():
        treeStr = treeStr.replace(oldDef,newDef)
    outTree.write(treeStr)
else:
    print("ERROR!")
    sys.exit()







inpTree.close()
inpFasta.close()
outTree.close()
outTree.close()