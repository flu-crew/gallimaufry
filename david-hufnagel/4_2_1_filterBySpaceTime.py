#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script takes a specific fasta file and creates a new one without N.
American sequences or sequences since Sep 3, 2020
Created by David E. Hufnagel on Jan  9, 2023
"""
import sys

inp = open("n1_v2_restoreSdup.fna")
out = open("n1_v2_restoreSdup_globalWtimeFilt.fna","w")





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

def FormatDate(oldDate):
    dateLst = oldDate.split("/")
    if len(dateLst) == 3:
        month = int(dateLst[0])
        day = int(dateLst[1])
        year = int(dateLst[2])
        newDate = "%s-%s-%s" % (year,month,day)
    elif len(dateLst) == 2:
        month = int(dateLst[0])
        year = int(dateLst[1])
        newDate = "%s-%s" % (year,month)
    elif len(dateLst) == 1:
        year = int(dateLst[0])
        newDate = "%s" % (year)
    else:
        print("ERROR!")
        print(dateLst)
        sys.exit()
    return(newDate)





#BODY
inpDict = ReadFasta(inp)
for defline, seqs in inpDict.items():
    if len(seqs) > 1:
        print("ERROR!")
        sys.exit()
    else:
        seq = seqs[0]
        defLst = defline.split("|")
        cntry = defLst[4]
        if cntry not in ["Canada","Costa_Rica","Cuba","Guatemala","Mexico","USA","Unknown"]:
            date = defLst[-1]
            if date != "NA":
                newDate = FormatDate(date)
                year = int(newDate.split("-")[0])
                if year < 2021:
                    newDateLst = newDate.split("-")
                    #set these to 1 so that seqs are kept when only year is provided
                    month = 1; day = 1
                    if len(newDateLst) == 3:
                        month = int(newDateLst[1])
                        day = int(newDateLst[2])
                    elif len(newDateLst) == 2:
                        month = int(newDateLst[1])
                        day = 1 #using 1 here not to change the data in the defline, but to keep anything in Sep 2020, where the day is uncertain
                    if year == 2020:
                        if month <= 9:
                            if month == 9:
                                if day <= 3:
                                    newlines = ">%s\n%s\n" % (defline,seq)
                                    out.write(newlines)
                            else:
                                newlines = ">%s\n%s\n" % (defline,seq)
                                out.write(newlines)
                    else:
                        newlines = ">%s\n%s\n" % (defline,seq)
                        out.write(newlines)











inp.close()
out.close()