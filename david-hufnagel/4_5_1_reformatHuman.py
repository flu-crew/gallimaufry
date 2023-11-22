#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 09:27:59 2023

@author: david.hufnagel
"""
import sys
inp = open("humanSeqsRaw_noDdup_markedDup.fasta")
out = open("humanSeqsRaw_noDdup_markedDup_reformat.fna", "w")





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
        
        strain = defLst[0].replace("'","_").replace("-","_").replace(".","_")\
            .replace("?","_").replace("(","_").replace(")","_")\
                .replace("&","_").replace("天津","Tianjin")
                
        sub = defLst[1].replace("N2v","N2")
        cntry = defLst[3]
        if "USA" in cntry:
            cntry = "USA"
                    
        clade = defLst[5]#.replace("gamma", "1A.3.3.3")
        date = defLst[6]
            
        newDef = "publicIAV|%s|%s|Human|%s|%s|%s" % \
            (strain, sub, cntry, clade, date)
        newlines = ">%s\n%s\n" % (newDef, seq)
        out.write(newlines)         












inp.close()
out.close()