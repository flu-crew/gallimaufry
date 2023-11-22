#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to 1) bring back lost variants, CVVs, and human 
seasonal strains 2) replace "'"s with "_"s in strain names because they're 
upsetting Figtree, and 3) Move A/swine/Kansas/A02245387/2020 from H1 to H3
Created by David E. Hufnagel on Aug  4, 2020
"""
import sys

oldH1 = open(sys.argv[1]) #allH1data.fna
oldH3 = open(sys.argv[2]) #allH3data.fna
inpH1 = open(sys.argv[3]) #allH1data_dateFilt_ambigFilt_noDup_wClades_wCons.fna
inpH3 = open(sys.argv[4]) #allH3data_dateFilt_ambigFilt_noDup_wClades_wCons.fna
outH1 = open(sys.argv[5], "w") #allH1data_dateFilt_ambigFilt_noDup_wClades_wCons_clean.fna
outH3 = open(sys.argv[6], "w") #allH3data_dateFilt_ambigFilt_noDup_wClades_wCons_clean.fna



def ExtractNonPublic(fd):
    humanDict = {}
    isGood = False #whether or not to store a seq in the dict
    lastDefline = ""
    lastSeq = ""
    for line in fd:
        if line.startswith(">"):
            #process last seq and reset variables
            if isGood:
                newLastDefline = "%s|human|%s" % ("|".join(lastDefline.split("|")[:4]), "|".join(lastDefline.split("|")[4:]))
                humanDict[newLastDefline] = lastSeq
            lastDefline = line
            lastSeq = ""
                
            
            #process current line
            lineLst = line.strip().strip(">").split("|")
            source = lineLst[0]
            if source != "publicIAV":
                isGood = True
            else:
                isGood = False
        else:
            if isGood:
                lastSeq += line.strip()
    else:
        if isGood:
            newLastDefline = "%s|human|%s" % ("|".join(lastDefline.split("|")[:4]), "|".join(lastDefline.split("|")[4:]))
            humanDict[newLastDefline] = lastSeq
            
    return(humanDict)



#Go through oldH1 and store variants, CVVs, and human seasonal strains in a
#  dict of key: defline val: seq
h1HumanDict = ExtractNonPublic(oldH1)

#Go through oldH3 and store variants, CVVs, and human seasonal strains in a
#  dict of key: defline val: seq
h3HumanDict = ExtractNonPublic(oldH3)

#Go through inpH1, when A/swine/Kansas/A02245387/2020 is found store its info
#  in [defline, seq], replace "'"s with "_"s in strain names where necessary,
#  output most lines as-is.
transfer = ["",""]
toTransfer = False
isGood = False #whether or not to output seq
lastDefline = ""
lastSeq = ""
for line in inpH1:
    if line.startswith(">"):
        lineLst = line.strip(">").strip().split("|")
        if not "consensus" in line:
            strain = lineLst[1]
            #transfer Kansas strain without losing the one that came right before
            if strain == "A/swine/Kansas/A02245387/2020":
                newDefline = "|".join([lineLst[0],lineLst[1], "H3N2", lineLst[3], \
                                       "unknown", lineLst[5], lineLst[6]])
                transfer[0] = newDefline
                
                #process last seq and reset variables
                if isGood:
                    newlines = "%s%s\n" % (lastDefline.replace("'","_"), lastSeq)
                    outH1.write(newlines)
                
                lastDefline = line
                lastSeq = ""  
                
                toTransfer = True
                isGood = False
                
            else:
                #process last seq and reset variables
                if isGood:
                    newlines = "%s%s\n" % (lastDefline.replace("'","_"), lastSeq)
                    outH1.write(newlines)
                
                lastDefline = line
                lastSeq = ""
                    
                toTransfer = False
                isGood = True
            
        else:
            #process last seq and reset variables
            if isGood:
                newlines = "%s%s\n" % (lastDefline.replace("'","_"), lastSeq)
                outH1.write(newlines)
            
            lastDefline = line
            lastSeq = ""
                
            toTransfer = False
            isGood = True
    else:
        if toTransfer:
            transfer[1] += line.strip()
        elif isGood:
            lastSeq += line.strip()
else:
    if isGood:
        newlines = "%s%s\n" % (lastDefline.replace("'","_"), lastSeq)
        outH1.write(newlines) 


#add in variants, CVVs, and human seasonal strains at the end
for defline, seq in h1HumanDict.items():
        newlines = "%s%s\n" % (defline, seq)
        outH1.write(newlines) 


#add in A/swine/Kansas/A02245387/2020 to H3
newlines = ">%s\n%s\n" % (transfer[0], transfer[1])
outH3.write(newlines)


#Go through inpH3, , replace "'"s with "_"s in strain names where necessary, 
#  output most lines as-is, and add in variants, CVVs, and human seasonal 
#  strains at the end
isGood = False #whether or not to output seq
lastDefline = ""
lastSeq = ""
for line in inpH3:
    if line.startswith(">"):
        lineLst = line.strip(">").strip().split("|")
        if not "consensus" in line:
            strain = lineLst[1]
            #process last seq and reset variables
            if isGood:
                newlines = "%s%s\n" % (lastDefline.replace("'","_"), lastSeq)
                outH3.write(newlines)
            
            lastDefline = line
            lastSeq = ""
            isGood = True
            
        else:
            #process last seq and reset variables
            if isGood:
                newlines = "%s%s\n" % (lastDefline.replace("'","_"), lastSeq)
                outH3.write(newlines)
            
            lastDefline = line
            lastSeq = ""
            isGood = True
    else:
        if isGood:
            lastSeq += line.strip()
else:
    if isGood:
        newlines = "%s%s\n" % (lastDefline.replace("'","_"), lastSeq)
        outH3.write(newlines) 


#add in variants, CVVs, and human seasonal strains at the end
for defline, seq in h3HumanDict.items():
        newlines = "%s%s\n" % (defline, seq)
        outH3.write(newlines) 




"""
problems to solve:
    1) clade information is missing entirely from non-public IAV samples
    2) we still have duplicates (to solve later)
"""




oldH1.close()
oldH3.close()
inpH1.close()
inpH3.close()
outH1.close()
outH3.close()