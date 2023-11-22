#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adds collected variants to existing data set along with Tavis' latest 
classifications.  Also rope in new context strains
Created by David E. Hufnagel on Fri Jul 16 10:57:50 2021
"""
import sys
inpH1 = open("mergedSeqs_v4_h1_plusVars1_wSomeClades.fna")
inpH3 = open("mergedSeqs_v4_h3_plusVars1_wSomeClades.fna")
tavisDataH1 = open("tavisCladeDataH1.txt")
tavisDataH3 = open("tavisCladeDataH3.txt")
newVars = open("ZZ_newVariantData/newVars.fasta")
contextStrains = open("selection.fna")
outH1 = open("mergedSeqs_v5_h1.fna", "w")
outH3 = open("mergedSeqs_v5_h3.fna", "w")





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





#Go through clade data files and make dicts of key: strain  val: clade
cladeDictH1 = {}
tavisDataH1.readline()
for line in tavisDataH1:
    lineLst = line.strip().split("\t")
    strain = lineLst[0].split("|")[-6]
    clade = lineLst[1]
    if clade == "ND":
        clade = ""
    
    SaveIntoDict(strain, clade, cladeDictH1)


cladeDictH3 = {}
tavisDataH3.readline()
for line in tavisDataH3:
    lineLst = line.strip().split("\t")
    strain = lineLst[0].split("|")[-6]
    clade = lineLst[1]
    if clade == "ND":
        clade = ""
    
    
    SaveIntoDict(strain, clade, cladeDictH1)
    
    
#Go through input data files and output sequences with updated clade information
inpH1Dict = ReadFasta(inpH1)
for defline, seq in inpH1Dict.items():
    if len(seq) == 1:
        defLst = defline.split("|")
        strain = defLst[6]
        oldClade = defLst[-2]  
        
        if strain in cladeDictH1:
            tavClades = cladeDictH1[strain]
            if len(tavClades) < 2:
                tavClade = cladeDictH1[strain][0]
            else:
                print("ERROR 7!")
                sys.exit()
        else:
            tavClade = ""
        
        if oldClade == "":
            clade = tavClade
        elif tavClade == "":
            clade = oldClade
        elif oldClade == tavClade:
            clade = tavClade
        else:  #disagreement between old and now, believe Tavis
            clade = tavClade
            
        defLst[-2] = clade
        newDef = "|".join(defLst)
            
        newlines = ">%s\n%s\n" % (newDef, seq[0])
        outH1.write(newlines)


    else:
        print("ERROR 10!")
        sys.exit()
        
        
inpH3Dict = ReadFasta(inpH3)
for defline, seq in inpH3Dict.items():
    if len(seq) == 1:
        
        defLst = defline.split("|")
        strain = defLst[6]
        oldClade = defLst[-2]
     
        if strain in cladeDictH3:
            tavClades = cladeDictH3[strain]
            if len(tavClades) < 2:
                tavClade = cladeDictH3[strain][0]
            else:
                print("ERROR 11!")
                sys.exit()
        else:
            tavClade = ""
        
        if oldClade == "":
            clade = tavClade
        elif tavClade == "":
            clade = oldClade
        elif oldClade == tavClade:
            clade = tavClade
        else:  #disagreement between old and now, believe Tavis
            clade = tavClade
            
        defLst[-2] = clade
        newDef = "|".join(defLst)
            
        newlines = ">%s\n%s\n" % (newDef, seq[0])
        outH3.write(newlines)
    else:
        print("ERROR 12!")
        sys.exit()


#Go through new variant data, format it, add clade information, and output
#   the result
varDict = ReadFasta(newVars)
for defline, seq in varDict.items():
    if len(seq) == 1:
        defLst = defline.split("|")
        prov = "variant"
        strain = defLst[0]
        subtype = defLst[1][-4:]
        host = "Human"
        if strain == "A/Mecklenburg-Vorpommern/1/2021":
            cntry = "DEU"
        elif strain == "A/Denmark/1/2021":
            cntry = "DNK"
        elif strain in ["A/Iowa/02/2021","A/North_Carolina/15/2020"]:
            cntry = "USA"
        elif strain in ["A/Manitoba/01/2021_(H1N2)v","A/Manitoba/02/2021_(H1N1)v"]:
            cntry = "CAN"
            strain = strain.split("_")[0]
        date = defLst[-1]
        
        if strain in cladeDictH1:
            clade = cladeDictH1[strain]
        else:
            clade = ""

        
        newlines = ">%s||||||%s|%s|%s|%s|%s|%s\n%s\n" % (prov, strain, subtype, host, cntry, clade, date, seq[0])
        if subtype.startswith("H1"):
            outH1.write(newlines)
        elif subtype.startswith("H3"):
            outH3.write(newlines)
        else:
            print("ERROR 3!")
            sys.exit()
        
        
    else:
        print("ERROR 1!")
        sys.exit()


#Go through context strains, exclude a few, format it, add clade information,
#   and output the ruselt
contextDict = ReadFasta(contextStrains)
for defline, seq in contextDict.items():
    if len(seq) == 1:
        #print(defline)
        defLst = defline.split("|")
        prov = defLst[0]
        strain = defLst[2]
        subtype = defLst[-5]
        host = "Human"
        cntry = defLst[5]
        date = defLst[-1]
        oldClade = defLst[-2]

        if subtype.startswith("H1"):            
            if strain in cladeDictH1:
                tavClades = cladeDictH1[strain]
                if len(tavClades) < 2:
                    tavClade = cladeDictH1[strain][0]
                else:
                    print("ERROR 4!")
                    sys.exit()
            else:
                tavClade = ""
            
            if oldClade == "":
                clade = tavClade
            elif tavClade == "":
                clade = oldClade
            elif oldClade == tavClade:
                clade = tavClade
            else:  #disagreement between old and now, believe Tavis
                clade = tavClade
                
            newlines = ">%s||||||%s|%s|%s|%s|%s|%s\n%s\n" % (prov, strain, subtype, host, cntry, clade, date, seq[0])
            outH1.write(newlines)
        elif subtype.startswith("H3"):            
            if strain in cladeDictH3:
                tavClades = cladeDictH3[strain]
                if len(tavClades) < 2:
                    tavClade = cladeDictH3[strain][0]
                else:
                    print("ERROR 5!")
                    sys.exit()
            else:
                tavClade = ""
            
            if oldClade == "":
                clade = tavClade
            elif tavClade == "":
                clade = oldClade
            elif oldClade == tavClade:
                clade = tavClade
            else:  #disagreement between old and now, believe Tavis
                clade = tavClade
                
            newlines = ">%s||||||%s|%s|%s|%s|%s|%s\n%s\n" % (prov, strain, subtype, host, cntry, clade, date, seq[0])
            outH3.write(newlines)
        else:
            print("ERROR 6!")
            sys.exit()

    else:
        print("ERROR 2!")
        sys.exit()











inpH1.close()
inpH3.close()
tavisDataH1.close()
tavisDataH3.close()
newVars.close()
contextStrains.close()
outH1.close()
outH3.close()