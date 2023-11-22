#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is calculates the length of the longest sequence, then trims
All sequences by a percentage of said length
Created by David E. Hufnagel on Tue Sep 27 13:01:28 2022
"""
import sys, math
inp = open(sys.argv[1])        #The input unfiltered fasta file
out = open(sys.argv[2], "w")   #The output filtered fasta file
thresh = float(sys.argv[3])    #What percentage length threshold to use for trimming





#Define functions
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





#Iterate through the fasta file to determine the longest sequence
inpDict = ReadFasta(inp)
longestSeq = 0
for defline, seq in inpDict.items():
    if len(seq) == 1:
        if len(seq[0]) > longestSeq:
            if "N" in seq[0] or "n" in seq[0]: #account for N's in the sequence, treating them the same as a gap
                longestSeq = len(seq[0].replace("N","").replace("n",""))
            else:
                longestSeq = len(seq[0])
    else:
        print("ERROR 1!")
        sys.exit()
        
        
#Determine the minimum length of a sequence based on the given threshold
if thresh >= 0 and thresh <= 100:   
    minLen = math.ceil(thresh / 100 * longestSeq)
else:
    print("ERROR 3")
    sys.exit()


#Iterate through the fasta file again and output only the sequences with a
#  length at least as long as the threshold
for defline, seq in inpDict.items():
    #account for Ns
    if len(seq) == 1:
        if len(seq[0].replace("N","").replace("n","")) >= minLen:
            newlines = ">%s\n%s\n" % (defline, seq[0])
            out.write(newlines)
    else:
        print("ERROR 2!")
        sys.exit()





inp.close()
out.close()