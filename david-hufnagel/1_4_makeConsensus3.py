#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take a big fasta file, break it up into single 
clades, generate consensus seqs from those clades, and add them back into the 
big fasta.
Created by David E. Hufnagel on Aug 24, 2020
This version was created from the first version on Sep 15, 2020 to be most 
  useful for the current N1 analysis 
"""
import sys, os

inp = open(sys.argv[1])
out = open(sys.argv[2], "w")
groupsFd = open(sys.argv[3]) #the namesWgroups file used in MEGA



def SaveIntoDict(key, val, dictx):
    if key in dictx:
        dictx[key].append(val)
    else:
        dictx[key] = [val,]
        
        
#Transforms IQ-TREE modified deflines into their original forms
def TransformDefline(oldDef):
    oldDefLst = oldDef.strip().split("_")
    before = oldDefLst[0]
    date = "/".join(oldDefLst[-3:])
    if "like" not in oldDef:
        newStrain = "/".join(oldDefLst[1:-7])
        after = "|".join(oldDefLst[-7:-3])
    else:
        newStrain = "/".join(oldDefLst[1:-9])
        after = "%s_%s_%s" % ("|".join(oldDefLst[-9:-5]), oldDefLst[-5], oldDefLst[-4])     
        
    #some manual corrections for the real odd balls
    if "A02478739_a" in oldDef:
        newStrain = "A/swine/Illinois/A02478739_a/2019"
    elif "North_Caro" in oldDef:
        newStrain = newStrain.replace("North/Ca","North_Ca")
    elif "South_Caro" in oldDef:
        newStrain = newStrain.replace("South/Ca","South_Ca")
    elif "OH_18_7963" in oldDef:
        newStrain = "A/swine/Ohio/OH_18_7963/2018"
    elif "North_Dak" in oldDef:
        newStrain = newStrain.replace("North/Da","North_Da")
    elif "South_Dak" in oldDef:
        newStrain = newStrain.replace("South/Da","South_Da")
        
    newDef = "%s|%s|%s|%s" % (before, newStrain, after, date)
    
    return(newDef)

def IsItGood(clade, date, year):
    if clade in ["maraschino", "newBlack"]:
        if year == 2019:
            return(True)
        else:
            return(False)     
    elif clade in ["cayenne", "midnight", "clover", "blueberry"]:
        if year == 2020:
            return(True)
        else:
            return(False)   
    elif clade == "tangerine":
        month = int(date.split("/")[0])
        if year == 2020 or (year == 2019 and month >= 7):
            return(True)
        else:
            return(False)  
    else:
        print("ERROR!")
        sys.exit()
        
            
        
    




#Go through groups file and make a dict of key: defline val: groupColor
groupsDict = {}
for line in groupsFd:
    lineLst = line.strip().split("=")
    defline = TransformDefline(lineLst[0]); groupColor = lineLst[1]
    groupsDict[defline] = groupColor


#Go through inp and make a dict of key: groupColor val: [(def1, seq1),(def2,seq2)...]
fastaDict = {}  #dict of key: defline  val: seq
lastDef = ""; lastSeq = ""; lastClade = ""
isGood = False
for line in inp:
    if line.startswith(">"):
        if not "consensus" in line:
            defline = line.strip().strip(">")
            lineLst = defline.split("|")
            clade = groupsDict[defline]; date = lineLst[-1]
            year = int(date.split("/")[2])
            
            #save data
            if isGood:
                SaveIntoDict(lastClade, (lastDef,lastSeq), fastaDict)
            
            #reset isgood
            isGood = IsItGood(clade, date, year)
            
            lastDef = defline; lastClade = clade; lastSeq = ""
        else:
            isGood = False
    else:
        if isGood:
            lastSeq += line.strip()
else:
    if isGood:
        SaveIntoDict(lastClade, (lastDef,lastSeq), fastaDict)


os.system("mkdir SingleCladesSep15")
for clade, pairs in fastaDict.items():
    #Go through dict and make seperate fastas in a new folder for each clade
    cladeFileName = "SingleCladesSep15/%sOnly.fna" % (clade)
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
    consFileName = "SingleCladesSep15/%scons.fna" % (clade)
    newCommand = "smof consensus %s_aligned.fna > %s" % (cladeFileName[:-4], consFileName)
    os.system(newCommand)
    
    #Go through the consensus files and output the data into the output with new names
    consFileFd = open(consFileName)
    for line in consFileFd:
        if line.startswith(">"):
            newline =  ">%s_consensusRecent\n" % (clade)
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
groupsFd.close()