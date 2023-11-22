#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is intended to split the main fasta file by clade, keeping only
needed sequences for the distance matrix I'm making for Brian.  Also makes
files with only sequences from January to June 2020 for the sake of making 
recent censensus sequences.
Created by David E. Hufnagel on Thu Feb 25 14:57:36 2021
"""
import sys

inp = open("h1.fna")





def SaveIntoDict(key, val, dictx):
    if key in dictx:
        dictx[key].append(val)
    else:
        dictx[key] = [val,]





#Go through inp and store data in dict of key: clade val: (defline, seq).
#  Also make a similar dict but with only publicIAV sequences from January to 
#  June 2020
toKeep = False; cladeDict = {}
toKeepCons = False; consCladeDict = {}
lastName = ""; lastSeq = ""; lastClade = ""
lastNameCons = ""; lastSeqCons = ""; lastCladeCons = "" #This is probably not necessary, but is done to be careful
for line in inp:
    if line.startswith(">"):
        toKeep = False
        lineLst = line.strip().split("|")
        source = lineLst[0].strip(">")
        if source in ["CVV", "forHI", "huVaccine", "publicIAV", "variant"]:
            if len(lineLst) == 7:
                cntry = lineLst[5]
                if cntry in ["USA"]:
                    clade = lineLst[4]
                    if clade in ["1A.1.1", "1A.3.3.3", "1A.3.3.2", \
                                 "1B.2.2.1", "1B.2.2.2", "1B.2.1"]:
                        if lastName != "": #skip the first line for writing to the dict
                            lastData = (lastName, lastSeq)
                            SaveIntoDict(lastClade, lastData, cladeDict)
                        lastClade = clade
                        lastName = line.strip()
                        lastSeq = ""
                        toKeep = True
            
        #Make the fastas for consensus seq generation
        toKeepCons = False
        if source in ["forHI", "publicIAV"]:
            if len(lineLst) == 7:
                cntry = lineLst[5]
                if cntry in ["USA"]:
                    clade = lineLst[4]
                    if clade in ["1A.1.1", "1A.3.3.3", "1A.3.3.2", \
                                  "1B.2.2.1", "1B.2.2.2", "1B.2.1"]:
                        date = lineLst[-1]
                        if date.startswith("2020"):
                            if lastName != "": #skip the first line for writing to the dict
                                lastDataCons = (lastNameCons, lastSeqCons)
                                SaveIntoDict(lastCladeCons, lastDataCons, consCladeDict)
                            lastCladeCons = clade
                            lastNameCons = line.strip()
                            lastSeqCons = ""
                            toKeepCons = True
            
    else:
        if toKeep:
            lastSeq += line.strip()
            
        if toKeepCons:
            lastSeqCons += line.strip()
else:
    lastData = (lastName, lastSeq)
    SaveIntoDict(lastClade, lastData, cladeDict)
    
    lastDataCons = (lastNameCons, lastSeqCons)
    SaveIntoDict(lastCladeCons, lastDataCons, consCladeDict)
    

#Go through dict and output data to separate fasta files based on clade
for clade, data in cladeDict.items():
    outName = "h1_%s.fna" % (clade.replace(".","_"))
    outFd = open(outName, "w")
    
    for pair in data:
        newDef = "%s\n" % (pair[0]); newSeq = "%s\n" % (pair[1])
        outFd.write(newDef); outFd.write(newSeq)
        
    outFd.close()
    
    
#Do the same for sequences destined to be a part of consensus sequence generation
for clade, data in consCladeDict.items():
    outName = "h1_%s_forCons.fna" % (clade.replace(".","_"))
    outFd = open(outName, "w")
    
    for pair in data:
        newDef = "%s\n" % (pair[0]); newSeq = "%s\n" % (pair[1])
        outFd.write(newDef); outFd.write(newSeq)
        
    outFd.close()








inp.close()
















inp.close()