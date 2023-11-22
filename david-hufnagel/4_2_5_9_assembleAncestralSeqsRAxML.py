#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script takes a file with ancestral states from RAxML and a list of
critical nodes as input and creates a fasta file containing an
ancestral state for each critical node with the defline format:
CladeName|nodeID
Created by David E. Hufnagel on Fri Sep 29, 2023
"""
import sys

ancInp = open(sys.argv[1])
critNodesInp = open(sys.argv[2])
out = open(sys.argv[3], "w")





#Go through critNodesInp and make a dict of key: nodeNum  val: cladeName
nodeDict = {}
for line in critNodesInp:
    lineLst = line.strip().split("\t")
    nodeDict[lineLst[1]] = lineLst[0]


#Go through ancInp, convert nodeID to nodeNum, extract ancestral sequence,
#  extract cladeName using nodeDict, and output the formatted result for critical nodes
for line in ancInp:
    lineLst = line.strip().split("\t")
    nodeID = lineLst[0]; ancSeq = lineLst[1]
    nodeNum = nodeID.strip("Node")
    
    if  nodeNum in nodeDict:
        cladeName = nodeDict[nodeNum]
        
        newlines = ">%s|%s\n%s\n" % (cladeName, nodeID, ancSeq)
        out.write(newlines)








ancInp.close()
critNodesInp.close()
out.close()