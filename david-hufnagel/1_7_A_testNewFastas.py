#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created by David E. Hufnagel on Thu Feb 18 17:08:22 2021
"""
import sys

table = open(sys.argv[1])
h1 = open(sys.argv[2])
h3 = open(sys.argv[3])


tableStrains = []
table.readline()
for line in table:
    lineLst = line.strip().split("\t")
    strain = lineLst[0]
    tableStrains.append(strain)
    
    
for line in h1:
    #print(line)
    if line.startswith(">") and "onsensus" not in line:
        lineLst = line.strip().split("|")
        strain = lineLst[5]
        #print(strain)
        if strain in tableStrains:
            #print("here")
            print(line.strip())
            tableStrains.remove(strain)     
    #sys.exit()
print("\n\n\n")
            

for line in h3:
    if line.startswith(">") and "onsensus" not in line:
        lineLst = line.strip().split("|")
        strain = lineLst[5]
        if strain in tableStrains:
            #print("here")
            print(line.strip())
            tableStrains.remove(strain)    
print("\n\n\n")

print(tableStrains)
    
    
    
    
    
    
    
    
    
table.close()
h1.close()
h3.close()