#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to replace names in a tree with IDs using a reference
file where each line has this format: id      defline
Created by David E. Hufnagel on Aug 10, 2023
"""
import sys

refs = open(sys.argv[1])       #The reference file with defline IDs
inpTree = open(sys.argv[2])    #The tree file returned from IQ-TREE
out = open(sys.argv[3], "w")   #A new tree file with ID names





#Go through ref and make a dict of key: defline  val: id
nameChange = {}
for line in refs:
    lineLst = line.strip().split("\t")
    idName = lineLst[0]; defline = lineLst[1]
    nameChange[defline] = idName
    

#Go through inpTree and save it's data in a string
inpTreeLst = inpTree.readlines()
treeStr = ""
if len(inpTreeLst) == 1:
    treeStr = inpTreeLst[0]
else:
    for line in inpTreeLst:
        treeStr += line.strip()


#Go through the dict, replace the names in the inpTree, 
#   and output the result
for idName, defline in nameChange.items():    
    treeStr = treeStr.replace(idName, defline)
    
out.write(treeStr)





refs.close()
inpTree.close()
out.close()