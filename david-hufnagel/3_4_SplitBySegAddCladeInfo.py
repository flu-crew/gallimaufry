#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to used information from the octoFLU classifier to
split a fasta by segment/subtype and label the clade 
Created by David E. Hufnagel on May 18, 2022
"""
import sys
fastaFd = open(sys.argv[1])  #fasta file with all sequences
classFd = open(sys.argv[2])  #octoFLU classifier output file associated with the above fasta





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





#Go through classFd, make a dict of key: modName  val: (segment/subtype, clade)
#   and a set of segment/subtypes
classDict = {}
segs = set([])
for line in classFd:
    lineLst = line.strip().split("\t")
    modName = lineLst[0]; seg = lineLst[1]; clade = lineLst[-1]
    classDict[modName] = (seg, clade)
    segs.add(seg)


#Go through all segment/subtypes and make an output file for each
outs = {} #a dict of key: segment/subtype  val: outFd
for seg in segs:
    inpRoot = ".".join(sys.argv[1].split(".")[:-1])
    outName = "%s_%s.fasta" % (inpRoot, seg)
    outFd = open(outName, "w")
    outs[seg] = outFd
    

#Go through fastaFd, add clade info to the second position, and output to the
#   file that matches the segment/subtype
fastaDict = ReadFasta(fastaFd)
for defline, seq in fastaDict.items():
    if len(seq) != 1:
        print("ERROR!")
        sys.exit()
    else:
        modDef = defline.replace("[","_").replace("]","_").replace("|","_").replace(";","_")
        clade = classDict[modDef][1]
        plisn(defline)
        print(modDef)
        print(clade)
        print()
        










fastaFd.close()
classFd.close()