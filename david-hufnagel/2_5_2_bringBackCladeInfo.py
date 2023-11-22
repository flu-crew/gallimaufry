#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to add back in available clade info that was left out
in previous scripts
Created by David E. Hufnagel on Thu Jul 15 17:27:56 2021
"""
import sys
inpH1 = open("mergedSeqs_v4_h1_plusVars1.fna")
inpH3 = open("mergedSeqs_v4_h3_plusVars1.fna")
cladeDataP = open("publicData.fna")
cladeDataH1 = open("h1.fna")
cladeDataH3 = open("h3.fna")
cladeDataV = open("huVaccines.fna")
cladeDataUNM = open("UMN-shared_pdm.fasta")
cladeDataSyn = open("synthetic-seq-clean-HA-reclassified.fasta")
outH1 = open("mergedSeqs_v4_h1_plusVars1_wSomeClades.fna", "w")
outH3 = open("mergedSeqs_v4_h3_plusVars1_wSomeClades.fna", "w")





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





#Go through each file with clade information in it and create dictionaries for
#   H1 and H3 of key: strain  val: clade
cladesDict_H1 = {}; cladesDict_H3 = {}
cladeDictP = ReadFasta(cladeDataP)
cnt1 = 0
cnt3 = 0
for defline, seq in cladeDictP.items():
    defLst = defline.split("|")
    strain = defLst[1]
    subtype = defLst[2][:2]
    clade = defLst[-3]
    
    if clade == "1A.1+1C.1":
        clade = ""
    
    if subtype == "H1":
        cnt1 += 1
        SaveIntoDict(strain, clade, cladesDict_H1)
    elif subtype == "H3":
        cnt3 += 1
        SaveIntoDict(strain, clade, cladesDict_H3)
    else:
        print("ERROR 1!")
        sys.exit()


cladeDictH1 = ReadFasta(cladeDataH1)
for defline, seq in cladeDictH1.items():
    if "onsensus" not in defline:
        defLst = defline.split("|")
        strain = defLst[-6]
        subtype = defLst[-5][:2]
        clade = defLst[-2]

        if subtype == "H1":
            SaveIntoDict(strain, clade, cladesDict_H1)
        elif subtype == "H3":
            SaveIntoDict(strain, clade, cladesDict_H3)
        else:
            print("ERROR 2!")
            sys.exit()
        

cladeDictH3 = ReadFasta(cladeDataH3)
for defline, seq in cladeDictH3.items():
    if "onsensus" not in defline:
        defLst = defline.split("|")
        strain = defLst[-6]
        subtype = defLst[-5][:2]
        clade = defLst[-2]
        

        if subtype == "H1":
            SaveIntoDict(strain, clade, cladesDict_H1)
        elif subtype == "H3":
            SaveIntoDict(strain, clade, cladesDict_H3)
        else:
            print("ERROR 3!")
            sys.exit()


cladeDictV = ReadFasta(cladeDataV)
for defline, seq in cladeDictV.items():
    defLst = defline.split("|")
    strain = defLst[-6]
    subtype = defLst[3][:2]
    clade = defLst[-2]

    if subtype == "H1":
        SaveIntoDict(strain, clade, cladesDict_H1)
    elif subtype == "H3":
        SaveIntoDict(strain, clade, cladesDict_H3)
    else:
        if subtype not in ["mi",""]:  # mi comes from mixed
            print("ERROR 4!")
            sys.exit()


cladeDictUNM = ReadFasta(cladeDataUNM)
for defline, seq in cladeDictUNM.items():
    defLst = defline.split("|")
    strain = defLst[1]
    subtype = defLst[2][:2]
    clade = defLst[-3]

    if subtype == "H1":
        SaveIntoDict(strain, clade, cladesDict_H1)
    elif subtype == "H3":
        SaveIntoDict(strain, clade, cladesDict_H3)
    else:
        print("ERROR 5!")
        sys.exit()


cladeDictSyn = ReadFasta(cladeDataSyn)
for defline, seq in cladeDictSyn.items():
    defLst = defline.split("|")
    strain = defLst[1]
    subtype = defLst[2][:2]
    clade = defLst[-2]
    
    if subtype == "H1":
        SaveIntoDict(strain, clade, cladesDict_H1)
    elif subtype == "H3":
        SaveIntoDict(strain, clade, cladesDict_H3)
    else:
        print("ERROR 6!")
        sys.exit()


#Go through the input files, resolve where there may be multiple clade entries,
#   and output the present information including clade information
inp1Dict = ReadFasta(inpH1)
for defline, seq in inp1Dict.items():
    if len(seq) == 1:
        defLst = defline.split("|")
        if len(defLst) == 12:  #most strains
            strain = defLst[-6]
            if strain in cladesDict_H1:  #not all strains have clade information
                cladeSet = cladesDict_H1[strain]
                if "" in cladeSet:
                    cladeSet.remove("")
                    
                if len(cladeSet) == 1:  #only one clade
                    defLst[-2] = cladeSet[0]
                    newDef = "|".join(defLst)
                    newlines = ">%s\n%s\n" % (newDef, seq[0])
                elif len(cladeSet) == 0:  #no clade info
                    newlines = ">%s\n%s\n" % (defline, seq[0])
                else:
                    if len(set(cladeSet)) == 1: #all the same clade
                        defLst[-2] = cladeSet[0]
                        newDef = "|".join(defLst)
                        newlines = ">%s\n%s\n" % (newDef, seq[0])
                    else:  #disagreement between clade info --> treat as no info
                        newlines = ">%s\n%s\n" % (defline, seq[0])
            else:  #no clade info
                newlines = ">%s\n%s\n" % (defline, seq[0])
        elif len(defLst) == 6:  #newly added variants
            defLst = defline.split("|")
            prov = "variant"
            strain = defLst[1]
            subtype = defLst[2]
            host = "Human"
            cntry = defLst[4]
            date = defLst[5]

            newlines = ">%s||||||%s|%s|%s|%s||%s\n%s\n" % (prov, strain, subtype, host, cntry, date, seq[0])
        else:
            print("ERROR 8!")
            sys.exit()
            
        outH1.write(newlines)
    else:
        print("ERROR 7!")
        sys.exit()
        
        
inp3Dict = ReadFasta(inpH3)
for defline, seq in inp3Dict.items():
    if len(seq) == 1:
        defLst = defline.split("|")
        if len(defLst) == 12:  #most strains
            strain = defLst[-6]
            if strain in cladesDict_H3:  #not all strains have clade information
                cladeSet = cladesDict_H3[strain]
                if "" in cladeSet:
                    cladeSet.remove("")
                    
                if len(cladeSet) == 1:  #only one clade
                    defLst[-2] = cladeSet[0]
                    newDef = "|".join(defLst)
                    newlines = ">%s\n%s\n" % (newDef, seq[0])
                elif len(cladeSet) == 0:  #no clade info
                    newlines = ">%s\n%s\n" % (defline, seq[0])
                else:
                    if len(set(cladeSet)) == 1: #all the same clade
                        defLst[-2] = cladeSet[0]
                        newDef = "|".join(defLst)
                        newlines = ">%s\n%s\n" % (newDef, seq[0])
                    else:  #disagreement between clade info --> treat as no info
                        newlines = ">%s\n%s\n" % (defline, seq[0])
            else:  #no clade info
                newlines = ">%s\n%s\n" % (defline, seq[0])
        elif len(defLst) == 6:  #newly added variants
            defLst = defline.split("|")
            prov = "variant"
            strain = defLst[1]
            subtype = defLst[2]
            host = "Human"
            cntry = defLst[4]
            date = defLst[5]

            newlines = ">%s||||||%s|%s|%s|%s||%s\n%s\n" % (prov, strain, subtype, host, cntry, date, seq[0])
        else:
            print("ERROR 9!")
            sys.exit()
            
        outH3.write(newlines)
    else:
        print("ERROR 10!")
        sys.exit()














inpH1.close()
inpH3.close()
cladeDataP.close()
cladeDataH1.close()
cladeDataH3.close()
cladeDataV.close()
cladeDataUNM.close()
cladeDataSyn.close()
outH1.close()
outH3.close()