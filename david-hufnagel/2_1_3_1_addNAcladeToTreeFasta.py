#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to add NA clade annotation our phylogenetic 
tree, our classifyer tree, our fasta file, and our metadata table.
While I was at it I replaced all simplified deflines with proper deflines.
Created by David E. Hufnagel on Fri Mar 26 14:06:52 2021
"""
import sys

inpFastaCorr = open("allN1s_v3_aligned_reformat_trueNoMixed_noGaps.fna")                           # C
inpFastaSimp = open("allN1s_v3_aligned_reformat_trueNoMixed_noGaps_simp.fna")                      # S
inpTree = open("allN1s_v3_aligned_reformat_trueNoMixed_noGaps_aligned_colored_v2_reroot.treefile") # S
inpClass = open("allN1s_v3_aligned_reformat_trueNoMixed_noGaps_aligned_colored_classify.treefile") # S
inpMeta = open("../4_DataSheet/strainMetaData.txt")                                                # C
inpCladeInfo = open("9_Rnd9/namesWgroups.txt")                                                     # S
inpCladeCols = open("../2_PairPlots/cladeColors.txt")                                              #
outFasta = open("allN1s_v4.fna", "w")
outTree = open("allN1s_v4.treefile", "w")
outClass = open("allN1s_v4_classify.treefile", "w")
outMeta = open("../4_DataSheet/strainMetaData_v2.txt", "w")





def RestoreExtra(full, middle):
    newline = ""; start = False#; cnt = 0
    for ch in full:
        if start == False:
            if ch == "p":
                start = True
                newline += middle
                #      scnt += 1
            else:
                newline += ch
        else:
            if ch == "'":
                start = False
                newline += ch
                
    #ensure that whether or not newline has an endline character it has precisely 1 upon return
    newline = newline.strip("\n") + "\n"
                                        
                
    return(newline)





#Go through inpFastaSimp and store deflines and strains in a list
simpDefs = []; simpStrains = []
for line in inpFastaSimp:
    if line.startswith(">"):
        defline = line.strip().strip(">").replace("__","_")
        strain = "A_Swine" + "_".join(defline.split("Swine")[1].split("_")[:-2]).replace("__","_")
        simpDefs.append(defline)
        simpStrains.append(strain)


#Go through inpFastaCorr, align with simple lists, and create dicts of 
#  key: simpStrain  val: corrStrain as well as key: simpDef  val: corrDef
cnt = 0; fixStrainDict = {}; fixDefDict = {}
for line in inpFastaCorr:
    if line.startswith(">"):
        corrDef = line.strip().strip(">")
        corrStrain = corrDef.split("|")[1]
        
        simpDef = simpDefs[cnt]
        simpStrain = simpStrains[cnt]
        
        fixDefDict[simpDef] = corrDef
        fixStrainDict[simpStrain] = corrStrain
        
        cnt += 1


#Go through cladeColors and make a dict of key: cladeColor  val: NAclade
cladeColorDict = {}
for line in inpCladeCols:
    lineLst = line.strip().split("\t")
    color = lineLst[0]
    clade = lineLst[1]
    cladeColorDict[color] = clade


#Go through inpCladeInfo and make a dict of key: corrStrain  val: NAclade
strainToCladeDict = {}
for line in inpCladeInfo:
    lineLst = line.strip().split("=")
    simpDef = lineLst[0]
    simpStrain = "A_Swine" + "_".join(simpDef.split("Swine")[1].split("_")[:-2]).replace("__","_")
    corrStrain = fixStrainDict[simpStrain]
    color = lineLst[1]
    clade = cladeColorDict[color]
    
    strainToCladeDict[corrStrain] = clade


#Write title line for outMeta
title = "strain\tsubtype\tcollection_date\tcountry\tUS_state\tNA_clade\tUS_HA_clade\tglobal_HA_clade\tNA_accession\tNCBI_taxon_ID\thost\tpassage\n"
outMeta.write(title)

#Go through inpMeta and output to outMeta including NAclade
inpMeta.readline()
for line in inpMeta:
    lineLst = line.strip().split("\t")
    strain = lineLst[0]
    clade = strainToCladeDict[strain]
    lineLst.insert(5, clade)
    newline = "\t".join(lineLst) + "\n"
    outMeta.write(newline)


#Go through inpFastaCorr again and output to outFasta including NAclade
inpFastaCorr.seek(0)
for line in inpFastaCorr:
    if line.startswith(">"):
        lineLst = line.split("|")
        strain = lineLst[1]
        clade = strainToCladeDict[strain]
        lineLst.insert(5, clade)
        newline = "|".join(lineLst)
        outFasta.write(newline)
    else:
        outFasta.write(line)

#Go through inpTree and output to outTree including NAclade
##Deal with the first part where there is roughly one strain per line
outTree.write(inpTree.readline())
outTree.write(inpTree.readline())
outTree.write(inpTree.readline())
outTree.write(inpTree.readline())
line = ""
while line != ";\n":
    line = inpTree.readline().replace("__","_")
    if not line.startswith(";"):
        simpStrain = "A_Swine" + "_".join(line.split("Swine")[1].split("_")[:-2]).replace("__","_")
        corrStrain = fixStrainDict[simpStrain]
        clade = strainToCladeDict[corrStrain]
        simpDef = line.strip().strip(">").split("&")[0].strip("'[").replace("__","_")
        corrDef = fixDefDict[simpDef]
        newDefLst = corrDef.split("|"); newDefLst.insert(5,clade)
        newDef = "|".join(newDefLst)
        
        #now take all the extra that was removed to get simpDef and wrap it around newDef
        newline = RestoreExtra(line, newDef)
        outTree.write(newline)
else:
    outTree.write(";\n")
        
    
##Deal with the newick format tree
outTree.write(inpTree.readline())
outTree.write(inpTree.readline())
outTree.write(inpTree.readline())
line = inpTree.readline()
toReplace = False #an indicator as to whether I am between the "'"s, meaning where a strain is named.
oldDef = ""
for ch in line:
    if toReplace == False:
        if ch == "'":
            outTree.write("'")
            toReplace = True
        else:
            outTree.write(ch)
    else:
        if ch == "'":
            toReplace = False
            simpStrain = "A_Swine" + "_".join(oldDef.split("Swine")[1].split("_")[:-2]).replace("__","_")
            corrStrain = fixStrainDict[simpStrain]
            clade = strainToCladeDict[corrStrain]
            corrDef = fixDefDict[oldDef.replace("__","_")]
            newDefLst = corrDef.split("|"); newDefLst.insert(5,clade)
            newDef = "|".join(newDefLst)
            outTree.write(newDef)
            outTree.write("'")
            oldDef = ""
        else:
            oldDef += ch
####This causes problems where "'"s do not surround strain names, but I will be fixing that issue outside of this script in the input tree
        
##Deal with the rest of the file
for line in inpTree:
    outTree.write(line)


#Go through inpClass and output to outClass including NAclade (The same procedure as the treefile, sorry for the repetition)
##Deal with the first part where there is roughly one strain per line
outClass.write(inpClass.readline())
outClass.write(inpClass.readline())
outClass.write(inpClass.readline())
outClass.write(inpClass.readline())
line = ""
while line != ";\n":
    line = inpClass.readline().replace("__","_")
    if not line.startswith(";"):
        simpStrain = "A_Swine" + "_".join(line.split("Swine")[1].split("_")[:-2]).replace("__","_")
        corrStrain = fixStrainDict[simpStrain]
        clade = strainToCladeDict[corrStrain]
        simpDef = line.strip().strip(">").split("&")[0].strip("'[").replace("__","_")
        corrDef = fixDefDict[simpDef]
        newDefLst = corrDef.split("|"); newDefLst.insert(5,clade)
        newDef = "|".join(newDefLst)
        
        #now take all the extra that was removed to get simpDef and wrap it around newDef
        newline = RestoreExtra(line, newDef)
        outClass.write(newline)
else:
    outClass.write(";\n")
        
    
##Deal with the newick format tree
outClass.write(inpClass.readline())
outClass.write(inpClass.readline())
outClass.write(inpClass.readline())
line = inpClass.readline()
toReplace = False #an indicator as to whether I am between the "'"s, meaning where a strain is named.
oldDef = ""
for ch in line:
    if toReplace == False:
        if ch == "'":
            outClass.write("'")
            toReplace = True
        else:
            outClass.write(ch)
    else:
        if ch == "'":
            toReplace = False
            simpStrain = "A_Swine" + "_".join(oldDef.split("Swine")[1].split("_")[:-2]).replace("__","_")
            corrStrain = fixStrainDict[simpStrain]
            clade = strainToCladeDict[corrStrain]
            corrDef = fixDefDict[oldDef.replace("__","_")]
            newDefLst = corrDef.split("|"); newDefLst.insert(5,clade)
            newDef = "|".join(newDefLst)
            outClass.write(newDef)
            outClass.write("'")
            oldDef = ""
        else:
            oldDef += ch
####This causes problems where "'"s do not surround strain names, but I will be fixing that issue outside of this script in the input tree
        
##Deal with the rest of the file
for line in inpClass:
    outClass.write(line)











inpFastaCorr.close()
inpFastaSimp.close()
inpTree.close()
inpClass.close()
inpMeta.close()
inpCladeInfo.close()
inpCladeCols.close()
outFasta.close()
outTree.close()
outClass.close()
outMeta.close()
