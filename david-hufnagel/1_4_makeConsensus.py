#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take a big fasta file, break it up into single 
clades, generate consensus seqs from those clades, and add them back into the 
big fasta.
Created by David E. Hufnagel on Aug 24, 2020
"""
import sys, os

inp = open(sys.argv[1])
out = open(sys.argv[2], "w")



def SaveIntoDict(key, val, dictx):
    if key in dictx:
        dictx[key].append(val)
    else:
        dictx[key] = [val,]
        


#Go through inp and make a dict of key: clade val: [(def1, seq1),(def2,seq2)...]
fastaDict = {}  #dict of key: defline  val: seq
lastDef = ""; lastSeq = ""; lastClade = ""
isGood = False
for line in inp:
    if line.startswith(">"):
        defline = line.strip().strip(">")
        lineLst = defline.split("|")
        source = lineLst[0]; clade = lineLst[4]; date = lineLst[-1]
        year = int(date.split("-")[0])
        
        #save data
        if isGood:
            SaveIntoDict(lastClade, (lastDef,lastSeq), fastaDict)
        
        #reset isgood
        if lastDef != "":
            if source in ["forHI", "offlu", "publicIAV"] and year == 2020:
                isGood = True
            else:
                isGood = False
        else:
            if source in ["forHI", "offlu", "publicIAV"] and year == 2020:
                isGood = True
            else:
                isGood = False
        lastDef = defline; lastClade = clade; lastSeq = ""
    else:
        if isGood:
            lastSeq += line.strip()
else:
    if isGood:
        SaveIntoDict(lastClade, (lastDef,lastSeq), fastaDict)


os.system("mkdir SingleCladesAug27")
for clade, pairs in fastaDict.items():
    #Go through dict and make seperate fastas in a new folder for each clade
    cladeFileName = "SingleCladesAug27/%sOnly.fna" % (clade)
    cladeFd = open(cladeFileName, "w")
    for pair in pairs:
        newline = ">%s\n" % (pair[0])
        cladeFd.write(newline)
        newline = "%s\n" % (pair[1])
        cladeFd.write(newline) 
    cladeFd.close()
    
    #Align fasta files
    newCommand = "mafft %s > %s_aligned.fna" % (cladeFileName, cladeFileName[:-4])
    os.system(newCommand)
    
    #Generate consensus seqs for each of these files using smof
    consFileName = "SingleCladesAug27/%scons.fna" % (clade)
    newCommand = "smof consensus %s_aligned.fna > %s" % (cladeFileName[:-4], consFileName)
    os.system(newCommand)
    
    #Go through the consensus files and output the data into the output with new names
    consFileFd = open(consFileName)
    for line in consFileFd:
        if line.startswith(">"):
            newline =  ">%s_consensus2020\n" % (clade)
            out.write(newline)
        else:
            out.write(line)
    consFileFd.close()

    
#Go through inp again and output all lines
inp.seek(0)
for line in inp:
    out.write(line)




inp.close()
out.close()
