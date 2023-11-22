#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to undo IQTREE's converting all "|"s and "/"s to "_"s
Created by David E. Hufnagel on Wed Aug 18 07:26:25 2021
"""
import sys

preIQfasta = open(sys.argv[1]) #The fasta file submitted to IQ-TREE
postIQtree = open(sys.argv[2]) #The tree file returned from IQ-TREE
out = open(sys.argv[3], "w")   #A new tree file with names fixed





#Go through preIQfasta, replace the "|"s in the names with "_"s and make a
#   dict of key: postName  val: preName
nameChange = {}
for line in preIQfasta:
    if line.startswith(">"):
        preName = line.strip().strip(">")
        postName = preName.replace("|","_").replace("/","_").replace("'","_").replace("+","_").replace("(","_").replace(")","_")
        nameChange[postName] = preName
    

#Go through postIQtree and save it's data in a string
postIQtreeLst = postIQtree.readlines()
if len(postIQtreeLst) == 1:
    postIQtreeStr = postIQtreeLst[0]
else:
    print("ERROR!")
    sys.exit()


#Go through the dict, replace replace the names in the postIQtree, 
#   and output the result
for postName, preName in nameChange.items():    
    postIQtreeStr = postIQtreeStr.replace(postName, preName)
    
out.write(postIQtreeStr)





preIQfasta.close()
postIQtree.close()
out.close()