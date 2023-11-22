#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to combine unpublished data with published data and 
all reference sequences from the last report for the sake of the fall 2021
OFFLU report.  Additional variants will be added in later.
Created by David E. Hufnagel on Tue Jul 13 11:43:51 2021
"""
import sys

publicFasta = open("publicData.fna")
unpubFasta = open("unpublishedSeqs_clean.fna")
febH1Fasta = open("h1.fna")
febH3Fasta = open("h3.fna")
vaccFasta = open("huVaccines.fna")
out = open("mergedSeqs_v1.fna", "w")
dups = open("dups.fna", "w")





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





#Import sequences from all fasta files, format them, and output them putting
#   most sequences in the main fasta file and defline duplicates in a
#   duplicates file
publicDict = ReadFasta(publicFasta)
dupID = 1
for defline, seq in publicDict.items():
    defLst = defline.split("|")
    prov = "publicIAV"
    strain = defLst[1]
    subtype = defLst[2]
    host = defLst[3]
    if host == "swine":
        host = "Swine"
    cntry = defLst[4]
    date = defLst[-1]
    
    if len(seq) == 1:
        newlines = ">%s||||||%s|%s|%s|%s||%s\n%s\n" % (prov, strain, subtype, host, cntry, date, seq[0])
        out.write(newlines)
    else:  #in all cases there were 2 seqs so I didn't control for other possibliities
        newlines = ">%s||||||%s|%s|%s|%s||%s__%s\n%s\n" % (prov, strain, subtype, host, cntry, date, dupID, seq[0])
        dups.write(newlines)
        dupID += 1 
        newlines = ">%s||||||%s|%s|%s|%s||%s__%s\n%s\n" % (prov, strain, subtype, host, cntry, date, dupID, seq[1])
        dups.write(newlines)
        dupID += 1


unpubDict = ReadFasta(unpubFasta)
for defline, seq in unpubDict.items():
    if len(seq) == 1:
        newDef = defline.replace("offlu-vcm|","offlu-vcm||||||").replace("syntheticIAV|","syntheticIAV||||||")
        newlines = ">%s\n%s\n" % (newDef, seq[0])
        out.write(newlines)
    else:
        print("ERROR 1!")
        sys.exit()
    

febH1Dict = ReadFasta(febH1Fasta)
for defline, seq in febH1Dict.items():
    if "onsensus" not in defline:
        defLst = defline.split("|")
        defLst.insert(5,"")
        
        prov = defLst[0]
        if prov in ["CVV", "SwReference", "huReference", "variant"]:
            
            if len(seq) == 1:
                newDef = "|".join(defLst)
                newlines = ">%s\n%s\n" % (newDef, seq[0])
                out.write(newlines)
            else:
                print("ERROR 2!")
                sys.exit()


febH3Dict = ReadFasta(febH3Fasta)
for defline, seq in febH3Dict.items():
    if "onsensus" not in defline:
        defLst = defline.split("|")
        defLst.insert(5,"")
        
        prov = defLst[0]
        if prov in ["CVV", "SwReference", "huReference", "variant"]:
            
            if len(seq) == 1:
                newDef = "|".join(defLst)
                newlines = ">%s\n%s\n" % (newDef, seq[0])
                out.write(newlines)
            else:
                print("ERROR 3!")
                sys.exit()
                

vaccDict = ReadFasta(vaccFasta)
for defline, seq in vaccDict.items():
    defLst = defline.split("|")
    prov = "huVaccine"
    strain = defLst[2]
    subtype = defLst[3]
    host = "Human"
    cntry = defLst[5]
    date = defLst[-1]
    
    if subtype == "mixed":
        subtype = "H1"  #A/Beijing/262/1995 is the one labeled mixed and came in a file labeled "seasonal H1"
    elif subtype == "":
        subtype = "H3N2" #A/California/7/2004 and A/Wisconsin/67/2005 have no subtype but came in a file labeled "H3N2"
    
    if cntry == "":
        if "Hong_Kong" in strain:
            cntry = "HKG"
        else:
            print("ERROR 4!")
            sys.exit()
            
    if len(seq) == 1:
        newlines = ">%s||||||%s|%s|%s|%s||%s\n%s\n" % (prov, strain, subtype, host, cntry, date, seq[0])
        out.write(newlines)
    else:
        print("ERROR 5!")
        sys.exit()









publicFasta.close()
unpubFasta.close()
febH1Fasta.close()
febH3Fasta.close()
out.close()
