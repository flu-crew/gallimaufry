#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script reformats global data for the N1 diversity project to match the
format of the main N. American data
Created by David E. Hufnagel on Jan 10, 2023
"""
import sys

inp = open("n1_global_v3.fna")
out = open("n1_global_v3_reformat.fna", "w")





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





#BODY
inpDict = ReadFasta(inp)
for defline, seqs in inpDict.items():
    if len(seqs) > 1:
        print("ERROR!")
        sys.exit()
    else:
        seq = seqs[0]
        defLst = defline.split("|")
        strain = defLst[0].replace("/pig/","/Swine/").replace("/sw/","/Swine/")\
            .replace("/swine/","/Swine/").replace("/Sw/","/Swine/")
        sub = defLst[2]; host = defLst[3]; cntry = defLst[4]; clade = defLst[5]
        date = defLst[6]
        newlines = ">publicIAV|%s|%s|%s|%s||%s|%s\n%s\n" % \
            (strain,sub,host,cntry,clade,date,seq)
        out.write(newlines)










inp.close()
out.close()