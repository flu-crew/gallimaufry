#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to trim sequences based on ORFs and a MSA
Created by David E. Hufnagel on Oct 15, 2020
"""
import sys

inp = open(sys.argv[1])      #input alignment file
out = open(sys.argv[2], "w") #trimmed output alignment file
startCoord = int(sys.argv[3]) #the coordinate of the first base in the start codon (vim style, meaning starting at 1)
stopCoord = int(sys.argv[4]) #the coordinate of the first base in the stop codon (vim style, meaning starting at 1)



def TrimSeq(seq):
    cnt = 1
    newSeq = ""
    for base in seq:
        if cnt >= startCoord and cnt <= stopCoord+2:
            newSeq += seq[cnt-1]
        cnt += 1
    
    return(newSeq)





#Go through alignment file, take in deflines and seqs, trim seqs, and output
#  the result in a list of lists where the outer list maintains the original
#  order and the innner list contains [defline, seq]
alignLst = []; lastDef = ""; lastSeq = ""
for line in inp:
    if line.startswith(">"):
        defline = line.strip().strip(">")
        if lastDef != "":
            #modify lastSeq by trimming
            trimmedSeq = TrimSeq(lastSeq)
            
            pair = [lastDef, trimmedSeq]
            alignLst.append(pair)
            
        lastDef = defline
        lastSeq = ""
        
    else:
        lastSeq += line.strip()
else:
    trimmedSeq = TrimSeq(lastSeq)
    
    pair = [lastDef, trimmedSeq]
    alignLst.append(pair)
        
        
#Go through the list and output the data into the new alignment file
for pair in alignLst:
    newline = ">%s\n" % (pair[0])
    out.write(newline)
    
    newline = "%s\n" % (pair[1])
    out.write(newline)





inp.close()
out.close() 
