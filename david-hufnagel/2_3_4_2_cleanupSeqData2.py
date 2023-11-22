#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to cleanup gammaSeqs06-16.fna and make sure they have
the proper format in preperation for downstream analysis.
Created by David E. Hufnagel on Thu May 27 15:09:01 2021
Modified on June 2, 2021 to use the file gammaSeqs20_21.fna
"""
import sys

inp = open("gammaSeqs20_21.fna")
out = open("gammaSeqs20_21_clean.fna", "w")
dupsOut = open("dups.fna", "w")



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


#Go through inp and store the file in a dict of key: defline   val: seq
fastaDict = ReadFasta(inp)


#Go through fastaDict, clean up strain names and identify duplicate strain
#   names storing the cleaned up names in a new dict with the same structure.
#   Also make a seperate dict for defline duplicates to be worked out more
#   manually
fastaDict2 = {}
defDups = {}
allStrains = []
strainDups = {}
for defline, seq in fastaDict.items():
    strain = defline.split("|")[0]
    
    #investigate duplicate deflines
    if len(seq) == 1:       
        if strain != "A/air/Ohio/13TOSU6529/2013":
            if strain not in allStrains:
                allStrains.append(strain)
            else:
                SaveIntoDict(strain, seq, strainDups)      
            
            fastaDict2[defline] = seq[0]
        
    elif len(seq) == 2:
        if seq[0] == seq[1]:  #defline and seq are both the same, just grab the first
            if strain not in allStrains:
                allStrains.append(strain)
            else:             #so here the 2 deflines are the same and so are the seqs, additionally the strain name matches with what's in another defline
                SaveIntoDict(strain, seq[0], strainDups)  
                
            fastaDict2[defline] = seq[0]
        else:                               #defline are the same, but seq is different
            SaveIntoDict(defline, seq[0], defDups)  
            SaveIntoDict(defline, seq[1], defDups)
    elif len(seq) == 3:
        if not seq[0] == seq[1] == seq[2]:  #defline are the same, but seq is different
            SaveIntoDict(defline, seq[0], defDups) 
            SaveIntoDict(defline, seq[1], defDups) 
            SaveIntoDict(defline, seq[2], defDups) 
        else:                   #defline seq are both the same, just grab the first
            print("ERROR1!")   
            sys.exit()
    else:
        print("ERROR2!")
        sys.exit()

                
#Go through fastaDict2, reformat, and output all the seqs that are not defDups or strainDups
for defline, seq in fastaDict2.items():
    strain = defline.split("|")[0]
    if strain not in strainDups:
        lineLst = defline.strip().split("|")
        source = "publicIAV"
        subtype = lineLst[1]
        host = lineLst[2]
        country = lineLst[3]
        clade = lineLst[4]
        date = lineLst[5]
        
        if "ixed" not in subtype:
            dateLst = date.split("/")
            if len(dateLst) == 2:
                date = "%s-%s" % (dateLst[1], dateLst[0])
            elif len(dateLst) == 3:
                date = "%s-%s-%s" % (dateLst[2], dateLst[0], dateLst[1])
            elif len(dateLst) != 1:
                print("ERROR3!")
                sys.exit()
        
            #fix strain name issues
            strain = strain.replace("//","/")
            
            newline = ">%s|%s|%s|%s|%s|%s|%s\n" % (source, strain, subtype, host, country, clade, date)
            out.write(newline)
            newline = "%s\n" % (seq)
            out.write(newline)


#Go through fasta again and add strain dups to the defline duplicates dict
for defline, seqs in fastaDict.items():
    strain = defline.split("|")[0]
    for seq in seqs:
        if strain in strainDups.keys():
            SaveIntoDict(defline, seq, defDups)
            

#Go through defDups, reformat, and output all seqs in a duplicates file with unique names
cnt = 1 #used to distinguish defline dups from each other
for defline, seqs in defDups.items():
    for seq in seqs:
        newline = ">%s_%s\n%s\n" % (defline, cnt, seq)
        dupsOut.write(newline)
    
        cnt += 1





inp.close()
out.close()
dupsOut.close()