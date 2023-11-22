#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to remove duplicates from a fasta file
Created by David E. Hufnagel on Wed Jul 29, 2020
"""
import sys

inp = open(sys.argv[1])
out = open(sys.argv[2], "w")



def SaveIntoDict(key, val, dictx):
    if key in dictx:
        dictx[key].append(val)
    else:
        dictx[key] = [val,]



#save info into a dict
seenSeqs = {}  #dict of key: defline  val: seq
lastDef = ""
lastSeq = ""
for line in inp:
    if line.startswith(">"):
        defline = line.strip().strip(">")
        if lastDef != "":
            SaveIntoDict(lastDef, lastSeq, seenSeqs)
            lastSeq = ""
        lastDef = defline
    else:
        lastSeq += line.strip()
else:
    SaveIntoDict(lastDef, lastSeq, seenSeqs)

#Parse the dict, look for problems, and output the result
for defline, seqs in seenSeqs.items():
    #duplicates found
    if len(seqs) != 1:
        #if multiple seqs for one defline are not identical, delete both, otherwise move forward
        if len(set(seqs)) == 1:
            newline = ">%s\n%s\n" % (defline, seqs[0])
            out.write(newline)

    else:
        newline = ">%s\n%s\n" % (defline, seqs[0])
        out.write(newline)


inp.close()
out.close()