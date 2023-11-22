#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script combines a fasta file and a CSV file from BV-BRC to make a fasta
file with a reasonble format
Created by David E. Hufnagel on Mar 20, 2023
"""
import sys

inpFasta = open(sys.argv[1])  #input fasta file
inpCSV = open(sys.argv[2])    #input tabular data file
out = open(sys.argv[3], "w")  #output fasta file





#Define functions
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

def Year224(year2):
    if int(year2) < 30:
        year4 = "20" + year2
    else:
        year4 = "19" + year2
    return(year4)

def Month322(month3):
    if month3 == "Jan":
        return("01")
    elif month3 == "Feb":
        return("02")
    elif month3 == "Mar":
        return("03")
    elif month3 == "Apr":
        return("04")
    elif month3 == "May":
        return("05")
    elif month3 == "Jun":
        return("06")
    elif month3 == "Jul":
        return("07")
    elif month3 == "Aug":
        return("08")
    elif month3 == "Sep":
        return("09")
    elif month3 == "Oct":
        return("10")
    elif month3 == "Nov":
        return("11")
    elif month3 == "Dec":
        return("12")
    else:
        print("ERROR3!")
        print(month3)
        sys.exit()





###  BODY  ###
#Go through the CSV file and save metadata in a dict with the format key: ID  val: (strain, subtype, country, date)
metaDict = {}
inpCSV.readline()
for line in inpCSV:
    lineLst = line.strip().split("\t")
    iD = lineLst[0]; subtype = lineLst[21]
    strain = lineLst[15].replace("SWINE","Swine").replace("swine","Swine").replace("SW","Swine")
    cntry = lineLst[70]; date = lineLst[67]
    
    #set day, month, and year
    if "/" in date: #MM/DD/YY
        dateLst = date.split("/")
        day = dateLst[1].zfill(2); month = dateLst[0].zfill(2)
        year = Year224(dateLst[2])
    elif "-" in date:
        dateLst = date.split("-")
        if len(date) == 6: #MMM-YY
            day = ""; year = Year224(dateLst[1])
            month = Month322(dateLst[0])
        elif len(date) == 7: #YYYY-MM
            day = ""; month = dateLst[1]; year = dateLst[0]
        elif len(date) >= 8: #DD-MMM-YY
            day = dateLst[0].zfill(2); month = Month322(dateLst[1])
            year = Year224(dateLst[2])
        else:
            print("ERROR1!")
            print(len(date))
            print(date)
            sys.exit()
    else:
        day = ""; month = ""; year = date
            
    #build a standardized date from day, month, and year
    if day != "":
        newDate = "%s-%s-%s" % (year, month, day)
    elif month != "":
        newDate = "%s-%s" % (year, month)
    else:
        newDate = year
        
    #Save metadata into dict
    metaDict[iD] = (strain, subtype, cntry, newDate)


#Go through the fasta file, create new deflines using the metada dict and print to output
inpDict = ReadFasta(inpFasta)
for defline, seqs in inpDict.items():
    if len(seqs) > 1:
        print("ERROR2!")
        sys.exit()
    else:
        seq = seqs[0]
        iD = defline.strip().split("|")[-1].strip("]").strip()
        if iD not in metaDict:
            iD += "0"
            if iD not in metaDict:
                iD = iD.strip("0")
        newDef = "publicIAV|%s|%s|Swine|%s||%s" % (metaDict[iD][0], metaDict[iD][1], metaDict[iD][2], metaDict[iD][3])
        newLines = ">%s\n%s\n" % (newDef, seq)       
        out.write(newLines)






inpFasta.close()
inpCSV.close()
out.close()