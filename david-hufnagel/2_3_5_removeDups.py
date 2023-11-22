#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to remove duplicates from a fasta with our standard
format.
Created by David E. Hufnagel on Sun Jun 13 16:07:45 2021
"""
import sys

inp = open(sys.argv[1]) #fasta input
outFasta = open(sys.argv[2], "w") #main fasta output
outDups = open(sys.argv[3], "w") #duplicates output



def SaveIntoDict(key, val, dictx):
    if key in dictx:
        dictx[key].append(val)
    else:
        dictx[key] = [val,]


def ReadFasta(fd): #Go through input and store the file in a dict of key: strain   val: seq as well as a dict of key: strain  val: defline
    seqDict = {}; defDict = {}
    oldDef = ""; oldSeq = ""
    for line in fd:
        if line.startswith(">"):
            if oldSeq != "":
                oldStrain = oldDef.split("|")[1]
                matchStrain = "/".join(oldStrain.split("/")[2:]).upper()
                SaveIntoDict(matchStrain, oldSeq, seqDict)
                SaveIntoDict(matchStrain, oldDef, defDict)
                oldDef = line.strip().strip(">")
                oldSeq = ""
            else:
                oldDef = line.strip().strip(">")
        else:
            oldSeq += line.strip()
    else:
        oldStrain = oldDef.split("|")[1]
        matchStrain = "/".join(oldStrain.split("/")[2:]).upper()
        SaveIntoDict(matchStrain, oldSeq, seqDict)
        SaveIntoDict(matchStrain, oldDef, defDict)
    return(seqDict, defDict)


def ReadFasta2(fd): #Go through input and store the file in a dict of key: defline   val: seq
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



#strains involved in duplicates are stored in a list, and the rest is outputed
seqDict, defDict = ReadFasta(inp)
dupStrains = []
for strain, seq in seqDict.items():
    defline = defDict[strain]
    if len(seq) == 1:
        newlines = ">%s\n%s\n" % (defline[0], seq[0])
        outFasta.write(newlines)
    elif len(seq) == 2:
        if seq[0] == seq[1]:  
            if "Ref" in defline[0]:   #These cases are all IRD vs Ref strains and Ref strains are kept
                keepDef = defline[0]
                newlines = ">%s\n%s\n" % (keepDef, seq[0])
                outFasta.write(newlines)
            elif "Ref" in defline[1]: #These cases are all IRD vs Ref strains and Ref strains are kept
                keepDef = defline[1]
                newlines = ">%s\n%s\n" % (keepDef, seq[0])
                outFasta.write(newlines)
            else:                     #These cases are both IRD strains
                dupStrains.append(strain)
        else:  #the seqs are not the same, so add both of them to the dups list
            dupStrains.append(strain)          
    elif len(seq) == 3:
        dupStrains.append(strain) 


#Go through fasta again and output duplicate lines to the duplicate output and "false duplicates" to the main fasta file
inp.seek(0)
inpDict = ReadFasta2(inp)
cnt = 1  #an ID to distinguish identical deflines from each other
for defline, seq in inpDict.items():
    strain = defline.split("|")[1]
    if strain in dupStrains:
        if len(seq) == 1:  #this means the strains are the same but the deflines were different.  Check to see if the only difference is IRD vs Reference.  In such a case keep the reference
            newlines = ">%s\n%s\n" % (defline, seq[0])
            if (defDict[strain][0].split("|")[0] == "IRD" or defDict[strain][1].split("|")[0] == "IRD") \
                and (defDict[strain][0].split("|")[0].endswith("Ref") or defDict[strain][1].split("|")[0].endswith("Ref")): #the condition where one is IRD and the other is a reference
                if defline.split("|")[0].endswith("Ref"):
                    outFasta.write(newlines)
            else:
                newlines = ">%s_%s\n%s\n" % (defline, cnt, seq[0])
                outDups.write(newlines)
                cnt += 1
        elif len(seq) == 2:
            newlines = ">%s_%s\n%s\n" % (defline, cnt, seq[0])
            outDups.write(newlines)
            cnt += 1
            newlines = ">%s_%s\n%s\n" % (defline, cnt, seq[1])
            outDups.write(newlines)
            cnt += 1
        elif len(seq) == 3:
            newlines = ">%s_%s\n%s\n" % (defline, cnt, seq[0])
            outDups.write(newlines)
            cnt += 1
            newlines = ">%s_%s\n%s\n" % (defline, cnt, seq[1])
            outDups.write(newlines)
            cnt += 1            
            newlines = ">%s_%s\n%s\n" % (defline, cnt, seq[2])
            outDups.write(newlines)
            cnt += 1               







inp.close()
outFasta.close()
outDups.close()
