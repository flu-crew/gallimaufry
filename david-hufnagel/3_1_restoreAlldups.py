#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to combine all duplicates with all other sequences to
assess which should be kept in the context of the greater data set
Created by David E. Hufnagel on Dec 30, 2021
"""
import sys

h1Data = open("mergedSeqs_h1_v2_trim_clean.fna")
h3Data = open("mergedSeqs_h3_v2_trim_clean.fna")
dups = open("dups.fna")
dupsMeta = open("dups.fna_Final_Output_sorted.txt")
outH1 = open("mergedSeqs_h1_v2_trim_clean_wAlldups.fna", "w")
outH3 = open("mergedSeqs_h3_v2_trim_clean_wAlldups.fna", "w")





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





#Go through dupsMeta and create a dict of key: defline  val: subtype (H1 or H3)
subDict = {}
for line in dupsMeta:
    lineLst = line.split("\t")
    defline = lineLst[0]; sub = lineLst[-4]
    subDict[defline] = sub


#Go through dups and split the fasta into H1 and H3 piping the result into
#   the correct outputs
dupDict = ReadFasta(dups)
for defline, seq in dupDict.items():
    if len(seq) > 1:
        print("ERROR1!")
        sys.exit()
    else:
        sub = subDict[defline.replace("|","_")]
        newdef = "%s_dup%s" % ("_".join(defline.split("_")[:-1]), defline.split("_")[-1])
        newlines = ">%s\n%s\n" % (newdef, seq[0])
        if sub == "H1":
            outH1.write(newlines)
        elif sub == "H3":
            outH3.write(newlines)
        else:
            print("ERROR2!")
            sys.exit()
        
#Go through h1Data and pipe data into the H1 output
h1Dict = ReadFasta(h1Data)
for defline, seq in h1Dict.items():
    if len(seq) > 1:
        print("ERROR3!")
        sys.exit()
    else:
        newlines = ">%s\n%s\n" % (defline, seq[0])
        outH1.write(newlines)

#Go through h3Data and pipe data into the H3 output
h3Dict = ReadFasta(h3Data)
for defline, seq in h3Dict.items():
    if len(seq) > 1:
        print("ERROR4!")
        sys.exit()
    else:
        newlines = ">%s\n%s\n" % (defline, seq[0])
        outH3.write(newlines)








h1Data.close()
h3Data.close()  
dups.close()
dupsMeta.close()
outH1.close()
outH3.close()   







