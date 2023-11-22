#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to do the final merge, which means adding newly
discovered variants in with the rest of the merged data.  This will also
create a first opportunity to get rid of defline duplicated from the current
merged file.  Finally this splits our merged file into H1 and H3.
Created by David E. Hufnagel on Wed Jul 14 19:17:19 2021
"""
import sys

mainFasta = open("mergedSeqs_v2.fna")
variantFastaH1 = open("combinedData_H1_clean_trim.aln")
variantFastaH3 = open("combinedData_H3_clean_trim.aln")
outH1 = open("mergedSeqs_v3_h1.fna", "w")
outH3 = open("mergedSeqs_v3_h3.fna", "w")
dupsH1 = open("dups_h1.fna", "w")
dupsH3 = open("dups_h3.fna", "w")





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





#Go through the main fasta file and pipe the result straight to the outputs
mainDict = ReadFasta(mainFasta)
dupID = 1
for defline, seq in mainDict.items():
    subtype = defline.split("|")[-5]
    
    if len(seq) == 1:
        newlines = ">%s\n%s\n" % (defline, seq[0])
        if subtype in ["H1","H1N1","H1N2"]:
            outH1.write(newlines)
        elif subtype in ["H3N1","H3N2"]:
            outH3.write(newlines)
        else:
            print("ERROR1!")
            sys.exit()
    else:  #all duplicates are duplicates of 2
        newlinesA = ">%s__%s\n%s\n" % (defline, dupID, seq[0])
        dupID += 1
        newlinesB = ">%s__%s\n%s\n" % (defline, dupID, seq[1])
        dupID += 1
        
        if subtype in ["H1","H1N1","H1N2"]:
            dupsH1.write(newlinesA)
            dupsH1.write(newlinesB)
        elif subtype in ["H3N1","H3N2"]:
            dupsH3.write(newlinesA)
            dupsH3.write(newlinesB)
        else:
            print("ERROR2!")
            sys.exit()


#Go through the variant H1 fasta file and pipe 2 specific strains to the 
#   outputs in the desired format
varH1Dict = ReadFasta(variantFastaH1)
for defline, seq in varH1Dict.items():
    if "A/North_Carolina/15/2020" in defline or "A/Wisconsin/03/2021" in defline:
        if len(seq) == 1:
            defLst = defline.split("|")
            prov = "variant"
            strain = defLst[1]
            subtype = defLst[2]
            host = defLst[3].capitalize()
            cntry = defLst[-2]
            date = defLst[-1]
            newlines = ">%s||||||%s|%s|%s|%s||%s\n%s\n" % (prov, strain, subtype, host, cntry, date, seq[0])
            outH1.write(newlines)
        else:
            print("ERROR3!")
            sys.exit()


#Go through the variant H3 fasta file and pipe 1 specific strain the outputs
#   in the desired format
varH3Dict = ReadFasta(variantFastaH3)
for defline, seq in varH3Dict.items():
    if "A/Wisconsin/01/2021" in defline:
        if len(seq) == 1:
            defLst = defline.split("|")
            prov = "variant"
            strain = defLst[1]
            subtype = defLst[2]
            host = defLst[3].capitalize()
            cntry = defLst[-2]
            date = defLst[-1]
            newlines = ">%s||||||%s|%s|%s|%s||%s\n%s\n" % (prov, strain, subtype, host, cntry, date, seq[0])
            outH3.write(newlines)
        else:
            print("ERROR4!")
            sys.exit()
















mainFasta.close()
variantFastaH1.close()
variantFastaH3.close()
outH1.close()
outH3.close()