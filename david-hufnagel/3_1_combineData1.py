#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to combine public and private data available for 
the purpose of consensus generation and strain selection for the Spring 2022
OFFLU-VCM report. This format is used for the output:
provenance|strain|subtype|host|country|clade|date 
where the date is in the format: YYYY-MM-DD

Created by David E. Hufnagel on Dec 28, 2021
"""
import sys


publicFD = open("publicSeqs.fna")
franceFD = open("PrivateData/frenchSeqs.fna")
franceMetaFD = open("PrivateData/frenchMetadata.csv") 
ukFD = open("PrivateData/ukSeqs.fna")
italyFD = open("PrivateData/italySeqs.fna")
italyMetaFD = open("PrivateData/italyMetadata.csv")
out = open("mergedSeqs_v1.fna", "w")





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





#Import public data, convert to new format without HI testing info
publicDict = ReadFasta(publicFD)
for defline, seq in publicDict.items():
    if len(seq) > 1:
        print("ERROR 1!")
        sys.exit()
    else:
        defLst = defline.split("|")
        strain = defLst[1].replace(" ","_"); subtype = defLst[2]
        host = defLst[3].capitalize(); cntry = defLst[4]; clade = defLst[5]
        date = defLst[-1]
        if not "+" in clade: # not mixed strains
            newlines = ">publicIAV|%s|%s|%s|%s|%s|%s\n%s\n" % \
                (strain, subtype, host, cntry, clade, date, seq[0])
            out.write(newlines)
    

#Import French metadata and save it into a dict of key: strain  val: date
franceMetaFD.readline()
franceMetaDict = {}
for line in franceMetaFD:
    lineLst = line.split(",")
    strain = lineLst[0].replace(" ","_").replace("'","_").split("(")[0].strip("_")
    date = lineLst[-5]
    franceMetaDict[strain] = date


#Import French data, convert to new format without HI testing info
franceDict = ReadFasta(franceFD)
for defline, seq in franceDict.items():
    if len(seq) > 1:
        print("ERROR 2!")
        sys.exit()
    else:
        defLst = defline.split("|")
        if defLst[-1] == "HA":
            strain = defLst[1].replace(" ","_"); host = "Swine"; cntry = "FRA"
            
            #correct for naming discrepancies
            if strain == "A/Sw/France/22-210302-1/2021":
                strain = "A/Sw/France/22-210302-2/2021"
            elif strain == "A/Sw/France/56-180424/2018_ech2":
                strain = "A/Sw/France/56-180424/2018"
                
            clade = ""; date = franceMetaDict[strain]
            
            subtype = defLst[2].replace("H1av","H1").replace("H1pdm","H1")\
                .replace("H1hu","H1").replace("N1pdm","N1")
            newlines = ">offlu-vcm|%s|%s|%s|%s|%s|%s\n%s\n" % \
                (strain, subtype, host, cntry, clade, date, seq[0])
            out.write(newlines)


#Import UK data, convert to new format without HI testing info
ukDict = ReadFasta(ukFD)
for defline, seq in ukDict.items():
    if len(seq) > 1:
        print("ERROR 3!")
        sys.exit()
    else:
        defLst = defline.split("|")
        strain = defLst[0].replace(" ","_"); subtype = defLst[1]
        host = "Swine"; cntry = "GBR"; clade = ""; date = "2021"
        
        newlines = ">offlu-vcm|%s|%s|%s|%s|%s|%s\n%s\n" % \
            (strain, subtype, host, cntry, clade, date, seq[0])
        out.write(newlines)


#Import Italian metadata and save it into a dict of key: strain  val: date
italyMetaFD.readline()
italyMetaDict = {}
for line in italyMetaFD:
    lineLst = line.split(",")
    strain = lineLst[0]
    date = lineLst[4]
    italyMetaDict[strain] = date

#Import Italian data, convert to new format without HI testing info
italyDict = ReadFasta(italyFD)
for defline, seq in italyDict.items():
    if len(seq) > 1:
        print("ERROR 4!")
        sys.exit()
    else:
        defLst = defline.split("/")
        #correct for discrepencies between metadata and fasta
        if len(defLst) == 7:
            defLst = [defLst[0],defLst[1],defLst[2],\
                      "-".join([defLst[3],defLst[4]]),defLst[5], defLst[6]]
        strain = "/".join(defLst[:-1]); subtype = defLst[-1]; host = "Swine"
        cntry = "ITA"; clade = ""; date = italyMetaDict[strain]
        
        newlines = ">offlu-vcm|%s|%s|%s|%s|%s|%s\n%s\n" % \
            (strain, subtype, host, cntry, clade, date, seq[0])
        out.write(newlines)



publicFD.close()
franceFD.close()
ukFD.close()
italyFD.close()
out.close()
franceMetaFD.close()
italyMetaFD.close()











