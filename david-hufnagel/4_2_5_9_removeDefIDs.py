#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script takes an id reference file, a fasta file with ID deflines, and a
tree file with ID deflines and replaces IDs with true names
Created by David E. Hufnagel on Sep 28, 2023
"""
import sys

idFd = open(sys.argv[1])     #reference connecting ID names with real names
inp = open(sys.argv[2])      #input tree with ID names
out = open(sys.argv[3], "w") #output tree with real names





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





#Go through the id file and make a dict of key: id  val: name
idDict = {}
for line in idFd:
    lineLst= line.strip().split("\t")
    idDict[lineLst[0]] = lineLst[1]


#Go through the tree file, save the whole thing in a string
inpTreeStr = ""
for line in inp:
    inpTreeStr += line


#replace all instances of the id with the name in that string and output the
#  string as the new tree file
for key, val in idDict.items():
    new_key = key + ":"
    new_val = val + ":"
    inpTreeStr = inpTreeStr.replace(new_key, new_val)
    if new_key in inpTreeStr:
        print(new_key)
        print("in")  #This let's me know it has multiple instances in the treefile and needs to be accounted for
        
out.write(inpTreeStr)









idFd.close()
inp.close()
out.close()