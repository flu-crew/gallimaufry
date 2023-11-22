#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script uses names files to correct gamma clade information in the version 
3 gamma fasta.
Created oby David E. Hufnagel on Aug 21, 2023
"""
import sys
c1namesFd = open("c1names.txt")
c2namesFd = open("c2names.txt")
c3namesFd = open("c3names.txt")
inpFasta = open("gammaSeqs_v3.aln")
out = open("gammaSeqs_v3_nameFix.aln", "w")





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


def ProcessNames(inpFd):
    for defline in inpFd:
        defLst = defline.strip().split("|")
        clade = defLst[-2]
        cladeDict[defline.strip()] = clade



#Go through each names file and make a dict of key: defline, val: clade
cladeDict = {}
ProcessNames(c1namesFd)
ProcessNames(c2namesFd)
ProcessNames(c3namesFd)


#Go through inpFasta, if defline is in the dict, replace the clade name with
#  the dict value, otherwise replace it with the base gamma clade. Output
#  the result
inpDict = ReadFasta(inpFasta)
for defline, seqs in inpDict.items():
    if len(seqs) > 1:
        print("ERROR!")
        sys.exit()
    else:
        seq = seqs[0]
        defLst = defline.strip().split("|")
        oldClade = defLst[-2]
        if defline in cladeDict:
            newClade = cladeDict[defline]
        else:
            newClade = "1A.3.3.3"
            
        defLst[-2] = newClade
        newlines = ">%s\n%s\n" % ("|".join(defLst), seq)
        out.write(newlines)






c1namesFd.close()
c2namesFd.close()
c3namesFd.close()
inpFasta.close()
out.close()