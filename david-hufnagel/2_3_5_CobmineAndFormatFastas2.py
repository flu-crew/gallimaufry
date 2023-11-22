#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script was designed to combine multiple fasta files into one file with a
consistent format, labeling sequences by their provenance and taking care to
have everything in the proper format.  Duplicates resulting from the merge and
strain duplicates will be handeled downstream, but some internal defline 
duplicates are handled here.
Created by David E. Hufnagel on Sun Jun 13 12:50:07 2021
Updated on June 16th, 2021 and associated with the folder:
    ~/Documents/2_Research/2_2021/3_gammaProject/5_gatherALLgammas/2_SecondTry
"""
import sys


mn99Fasta = open("MN99.fasta")
bigGammasFasta = open("allGammas.fna")
c1Refs = open("C1_subsampled_08222017_aln.fasta")
c2Refs = open("C2_subsampled_08222017_aln.fasta")
c3Refs = open("C3_subsampled_08222017_aln_v3.fasta")
out = open("allGammas_v2.fna", "w")



def SaveIntoDict(key, val, dictx):
    if key in dictx:
        dictx[key].append(val)
    else:
        dictx[key] = [val,]

def ReadFasta(fd): #Go through input and store the file in a dict of key: defline   val: seq
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



#Go through each fasta file, label, reformat, and output seqs
bigGammasDict = ReadFasta(bigGammasFasta)
cnt = 0
for defline, seq in bigGammasDict.items():
    lineLst = defline.strip().split("|")
    strain = lineLst[0]
    subtype = lineLst[1]
    host = lineLst[2]
    cntry = lineLst[3]
    clade = lineLst[4]
    date = lineLst[5]        
    
    if strain != "A/air/Ohio/13TOSU6529/2013":
        newStrain = strain
            
        if "ixed" not in subtype:
            dateLst = date.split("/")
            if len(dateLst) == 1:
                newDate = date
            elif len(dateLst) == 2:
                newDate = "%s-%s" % (dateLst[1], dateLst[0])
            elif len(dateLst) == 3:
                newDate = "%s-%s-%s" % (dateLst[2], dateLst[0], dateLst[1])
            else:
                print("ERROR1")
                sys.exit()
    
            if len(seq) == 1:                
                newDef = ">IRD|%s|%s|%s|%s|%s|%s\n" % (newStrain, subtype, host, cntry, clade, newDate)
                out.write(newDef)
                newSeq = "%s\n" % (seq[0])
                out.write(newSeq)
            elif len(seq) == 2:
                if seq[0] == seq[1]:  #defline and seq are both the same, just grab the first
                    newDef = ">IRD|%s|%s|%s|%s|%s|%s\n" % (newStrain, subtype, host, cntry, clade, newDate)
                    out.write(newDef)
                    newSeq = "%s\n" % (seq[0])
                    out.write(newSeq)
                else:                 #defline are the same, but seq is different
                    newDef = ">IRD|%s|%s|%s|%s|%s|%s\n" % (newStrain, subtype, host, cntry, clade, newDate)
                    out.write(newDef)
                    newSeq = "%s\n" % (seq[0])
                    out.write(newSeq)
                    out.write(newDef)
                    newSeq = "%s\n" % (seq[1])
                    out.write(newSeq)
            elif len(seq) == 3:
                if not seq[0] == seq[1] == seq[2]:  #defline are the same, but seq is different
                    newDef = ">IRD|%s|%s|%s|%s|%s|%s\n" % (newStrain, subtype, host, cntry, clade, newDate)
                    out.write(newDef)
                    newSeq = "%s\n" % (seq[0])
                    out.write(newSeq)
                    out.write(newDef)
                    newSeq = "%s\n" % (seq[1])
                    out.write(newSeq)
                    out.write(newDef)
                    newSeq = "%s\n" % (seq[2])
                    out.write(newSeq)
                else:                   #defline seq are both the same, just grab the first
                    print("ERROR2!")   
                    sys.exit()
                

for line in mn99Fasta:
    if line.startswith(">"):
        newDef = line.replace(">",">MN99Ref|")
        out.write(newDef)
    else:
        if line != "\n":
            out.write(line)


c1Dict = ReadFasta(c1Refs)
for defline, seq in c1Dict.items():  #there were no defline duplicates here so I didn't have to account for that
    lineLst = defline.strip().split("|")
    strain = lineLst[2].replace("A/swine","A/Swine")
    subtype = lineLst[3]
    host = lineLst[4]
    cntry = "USA"
    clade = "1A.3.3.3"
    date = lineLst[-1].strip("-")
    
    if host == "human":
        host = "Human"
        
    newDef = ">C1Ref|%s|%s|%s|%s|%s|%s\n" % (strain, subtype, host, cntry, clade, date)
    out.write(newDef)
    newSeq = "%s\n" % (seq[0])
    out.write(newSeq)


c2Dict = ReadFasta(c2Refs)
for defline, seq in c2Dict.items():  #there were no defline duplicates here so I didn't have to account for that
    lineLst = defline.strip().split("|")
    strain = lineLst[2].replace("A/swine","A/Swine")
    subtype = lineLst[3]
    host = lineLst[4]
    cntry = "USA"
    clade = "1A.3.3.3"
    date = lineLst[-1].strip("-")
    
    newDef = ">C2Ref|%s|%s|%s|%s|%s|%s\n" % (strain, subtype, host, cntry, clade, date)
    out.write(newDef)
    newSeq = "%s\n" % (seq[0])
    out.write(newSeq)


c3Dict = ReadFasta(c3Refs)
for defline, seq in c3Dict.items():  #there were no defline duplicates here so I didn't have to account for that
    lineLst = defline.strip().split("|")
    strain = lineLst[2].replace("A/swine","A/Swine")
    subtype = lineLst[3]
    host = lineLst[4]
    cntry = "USA"
    clade = "1A.3.3.3"
    date = lineLst[-1].strip("-")
    
    
    if host == "human":
        host = "Human"
    
    newDef = ">C3Ref|%s|%s|%s|%s|%s|%s\n" % (strain, subtype, host, cntry, clade, date)
    out.write(newDef)
    newSeq = "%s\n" % (seq[0])
    out.write(newSeq)








mn99Fasta.close()
bigGammasFasta.close()
c1Refs.close()
c2Refs.close()
c3Refs.close()
out.close()