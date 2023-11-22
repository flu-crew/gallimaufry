#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 09:27:59 2023

@author: david.hufnagel
"""
import sys
inp = open("gammaSeqs_v1_noDDup_addBack.fna")
out = open("gammaSeqs_v1_noDDup_addBack_reformat.fna", "w")





def SaveIntoDict(key, val, dictx):
    if key in dictx:
        dictx[key].append(val)
    else:
        dictx[key] = [val,]

def ReadFasta(fd): #Go through inp and store the file in a dict of key: defline   val: seq
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





inpDict = ReadFasta(inp)
for defline, seqs in inpDict.items():
    if len(seqs) != 1:
        print("ERROR1!")
        sys.exit()
    else:
        seq = seqs[0]
        defLst = defline.split("|")
        if defLst[0] not in ["publicIAV","variant"]:
            strain = defLst[0].replace("//","/").replace("Minnoosta", "Minnesota")\
                    .replace("Minneosta", "Minnesota").replace("Carollina", "Carolina")\
                        .replace("SouthDakota", "South_Dakota").replace("MI","Michigan")
            
            if "air" not in strain: #remove 'air' strain 
                sub = defLst[1]
                if sub == "":
                    sub = "H1"
                    
                cntry = defLst[3]
                if "USA" in cntry:
                    cntry = "USA"
                if cntry == "":
                    if 'Ohio' in strain or 'USA' in strain or 'United_States' in strain \
                        or 'Indiana' in strain or 'Minnesota' in strain:
                        cntry = "USA"
                    elif 'Guangxi' in strain or 'Guangdong' in strain:
                        cntry = "CHN"
                    elif 'Korea' in strain:
                        cntry = "KOR"
                    elif 'Hong_Kong' in strain:
                        cntry = "HKG"
                    else:
                        print("ERROR2!")
                        sys.exit()
                        
                clade = defLst[5]#.replace("gamma", "1A.3.3.3")
                if clade != "1A.3.2": #remove non-gamma strains
                    date = defLst[6]
                
                    newDef = "publicIAV|%s|%s|Swine|%s|%s|%s" % \
                        (strain, sub, cntry, clade, date)
                    newlines = ">%s\n%s\n" % (newDef, seq)
                    out.write(newlines)
        else:
            newlines = ">%s\n%s\n" % (defline.replace("||","|1A.3.3.3|"), seq) #This move is okay because grep tells me the only instance of "||" is the missing clades in variants
            out.write(newlines)            












inp.close()
out.close()