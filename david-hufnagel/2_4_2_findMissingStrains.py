#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to determine which sequences were present in the OFFLU
data set, but not Zeb's pull
Created by David E. Hufnagel on Thu Aug 12 11:13:45 2021
"""
import sys
allSeqsFasta = open("mergedData_3.2010.1_v2_wOK20.fna")
pullSeqsFasta = open("DeleteMe/2010.1_noDups_dupRestore.fna")
out = open("missingSeqs.fna", "w")





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





#Go through all seqs and make a list of strains
allStrains = []
strainsDict = {}
for line in allSeqsFasta:
    if line.startswith(">") and "onsensus" not in line:
        lineLst = line.strip().strip(">").split("|")
        numFields = len(lineLst)
        if numFields == 4:
            strain = lineLst[0]
        elif numFields == 7:
            strain = lineLst[1]
        elif numFields == 11 or numFields == 12:
            strain = lineLst[-6]
        else:
            print("ERROR 1!")
            sys.exit()
    
        allStrains.append(strain)
        strainsDict[strain] = line


#Go through pull seqs remove strains from the all seqs list
for line in pullSeqsFasta:
    if line.startswith(">") and "onsensus" not in line:
        lineLst = line.strip().strip(">").split("|")
        strain = lineLst[1]
        allStrains.remove(strain)
            
        
#Go through all seqs again and output data where strains remain in the strains
#  list
allSeqsFasta.seek(0)
allSeqsDict = ReadFasta(allSeqsFasta)
for defline, seq in allSeqsDict.items():
    if "onsensus" not in defline:
        lineLst = defline.strip().strip(">").split("|")
        numFields = len(lineLst)
        if numFields == 4:
            strain = lineLst[0]
        elif numFields == 7:
            strain = lineLst[1]
        elif numFields == 11 or numFields == 12:
            strain = lineLst[-6]
        else:
            print("ERROR 2!")
            sys.exit()
        
        if strain in allStrains:
            if len(seq) == 1:
                newlines = ">%s\n%s\n" % (defline, seq[0])
                out.write(newlines)
            else:
                print("ERROR 3!")
                sys.exit()
    






allSeqsFasta.close()
pullSeqsFasta.close()
out.close()