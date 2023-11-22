#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Thtis script is designed to assemble and reformat unpublished sequence data
for the fall 2021 OFFLU report.
Created by David E. Hufnagel on Mon Jul 12 12:13:35 2021
"""
import sys


ukFasta = open("Unpublished_InfluenzaA_UKswine_2020_2021_HA.fasta") #
ukMeta = open("VCM_data_UK_APHA_BM_SI.txt")
belFasta = open("belgiumNT.fna")                                    #
belMeta = open("Kopie van VCM_data_template_SI_ June2021.txt")
canFasta = open("canadaSeqs.fasta")                                 #includes NA sequences
canMeta = open("VCM_data_template_SI.txt")
itaFasta = open("VIRUSES_ITALY_2021-1_HA.fas")                      #
itaMeta = open("VCM_data_template_SI_2021-1_Italy.txt")
umnFasta = open("UMN-shared_pdm.fasta")                             #
jpnFasta = open("HA_IAV-S_NIAH_JPN_2021.fas")                       #
jpnMeta = open("VCM_data_IAV-S_NIAH_JPN_2021.txt")
synFasta = open("synthetic-seq-clean-HA-reclassified.fasta")        #
mainFasta = open("unpublishedSeqs.fna", "w")
#dups = open("dups.fna", "w")          #####    NO DEFLINE DUPLICATES WERE FOUND      #####





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





#Go through all metadata files and save all relavant information in dictionaries
ukMeta.readline()
ukMetaDict = {}  #key: strain  val: (subtype, date, country, host)
for line in ukMeta:
    lineLst = line.strip().split("\t")
    strain = lineLst[0]; subtype = lineLst[2]
    
    date = lineLst[3]; cntry = "GBR"; host = lineLst[5]
    val = (subtype, date, cntry, host)
    SaveIntoDict(strain, val, ukMetaDict)


canMeta.readline()
canMetaDict = {}  #key: strain  val: (subtype, date, country, host)
for line in canMeta:
    lineLst = line.strip().split("\t")
    
    #correct for strain names in the metadata not matching that in the fasta files
    strain = lineLst[0][:-5].replace("_","/").replace("A/sw/","A/swine/")    
    subtype = lineLst[3]; date = lineLst[4]; cntry = "CAN"; host = "Swine"
    val = (subtype, date, cntry, host)
    SaveIntoDict(strain, val, canMetaDict)


belMeta.readline()
belMetaDict = {}  #key: strain  val: (subtype, date, country, host)
for line in belMeta:
    lineLst = line.strip().split("\t")
    
    #correct for strain names in the metadata not matching that in the fasta files
    strain = lineLst[0]  
    subtype = lineLst[3].strip("p")
    date = lineLst[4]; cntry = "BEL"; host = "Swine"
    val = (subtype, date, cntry, host)
    SaveIntoDict(strain, val, belMetaDict)


itaMeta.readline()
itaMetaDict = {}  #key: strain  val: (subtype, date, country, host)
for line in itaMeta:
    lineLst = line.strip().split("\t")
    strain = lineLst[0].replace("_","/")
    if strain.count("/") == 5:
        strainLst = strain.split("/")
        strain = "%s/%s/%s/%s-%s/%s" % (strainLst[0], strainLst[1], \
                                        strainLst[2], strainLst[3], \
                                            strainLst[4], strainLst[5])
    
    subtype = lineLst[3]; date = lineLst[4]; cntry = "ITA"; host = "Swine"
    val = (subtype, date, cntry, host)
    SaveIntoDict(strain, val, itaMetaDict)


jpnMeta.readline()
jpnMetaDict = {}  #key: strain  val: (subtype, date, country, host)
for line in jpnMeta:
    lineLst = line.strip().split("\t")
    strain = lineLst[0]; subtype = lineLst[1]
    date = lineLst[2]; cntry = "JPN"; host = "Swine"
    val = (subtype, date, cntry, host)
    SaveIntoDict(strain, val, jpnMetaDict)


#Go through fastas one at a time, check that everything looks right, exclude
#   NA sequences where labeled, reformat and store them into a dict of key:
#   defline  val: seq
ukDict = ReadFasta(ukFasta)
for defline, seq in ukDict.items():
    strain = defline
    
    #grab info from metadata dictionary
    if len(ukMetaDict[strain]) == 1:
        subtype = ukMetaDict[strain][0][0]; date = ukMetaDict[strain][0][1]
        cntry = ukMetaDict[strain][0][2]; host = ukMetaDict[strain][0][3]
    else:
        print("ERROR 1!")
        sys.exit()
        
    #test for defline duplicates
    if len(seq) != 1:
        print("ERROR 1-2!")
        sys.exit()
        
    #output
    newlines = ">offlu-vcm|%s|%s|%s|%s||%s\n%s\n" % (strain, subtype, host, cntry, date, seq[0])
    mainFasta.write(newlines)
    
    
#print(belMetaDict)
belDict = ReadFasta(belFasta)
for defline, seq in belDict.items():
    strain = defline.split("|")[0]
    
    #grab info from metadata dictionary
    if len(belMetaDict[strain]) == 1:
        subtype = belMetaDict[strain][0][0]; date = belMetaDict[strain][0][1]
        cntry = belMetaDict[strain][0][2]; host = belMetaDict[strain][0][3]
    else:
        print("ERROR 7!")
        sys.exit()
        
    #test for defline duplicates
    if len(seq) != 1:
        print("ERROR 7-2!")
        sys.exit()
        
    #output
    newlines = ">offlu-vcm|%s|%s|%s|%s||%s\n%s\n" % (strain, subtype, host, cntry, date, seq[0])
    mainFasta.write(newlines)    
    

canDict = ReadFasta(canFasta)
for defline, seq in canDict.items():
    strain = defline.split("|")[0].replace("_","/").replace("A/sw/","A/swine/").replace("1064231","1064321")
    segment = defline.split("_")[-1]
    if segment == "HA":        
        #grab info from metadata dictionary
        if len(canMetaDict[strain]) == 1:
            subtype = canMetaDict[strain][0][0]; date = canMetaDict[strain][0][1]
            cntry = canMetaDict[strain][0][2]; host = canMetaDict[strain][0][3]
            strain += "/2021"
        else:
            print("ERROR 2!")
            sys.exit()
            
        #test for defline duplicates
        if len(seq) != 1:
            print("ERROR 2-2!")
            sys.exit()
        
        #output
        newlines = ">offlu-vcm|%s|%s|%s|%s||%s\n%s\n" % (strain, subtype, host, cntry, date, seq[0])
        mainFasta.write(newlines)

                 
itaDict = ReadFasta(itaFasta)
for defline, seq in itaDict.items():
    strain = defline.split("|")[0].replace("_","/")
    if strain.count("/") == 5:
        strainLst = strain.split("/")
        strain = "%s/%s/%s/%s-%s/%s" % (strainLst[0], strainLst[1], \
                                        strainLst[2], strainLst[3], \
                                            strainLst[4], strainLst[5])

    #grab info from metadata dictionary
    if len(itaMetaDict[strain]) == 1:
        subtype = itaMetaDict[strain][0][0]; date = itaMetaDict[strain][0][1]
        cntry = itaMetaDict[strain][0][2]; host = itaMetaDict[strain][0][3]
    else:
        print("ERROR 3!")
        sys.exit()
        
    #test for defline duplicates
    if len(seq) != 1:
        print("ERROR 3-2!")
        sys.exit()
        
    #output
    newlines = ">offlu-vcm|%s|%s|%s|%s||%s\n%s\n" % (strain, subtype, host, cntry, date, seq[0])
    mainFasta.write(newlines)
    
    
umnDict = ReadFasta(umnFasta)
for defline, seq in umnDict.items():
    defLst = defline.strip().split("|")
    strain = defLst[1]
    subtype = defLst[2]
    host = "Swine"
    cntry = defLst[5]
    date = defLst[6]
        
    #test for defline duplicates
    if len(seq) != 1:
        print("ERROR 4!")
        sys.exit()
    
    #output
    newlines = ">offlu-vcm|%s|%s|%s|%s||%s\n%s\n" % (strain, subtype, host, cntry, date, seq[0])
    mainFasta.write(newlines)


jpnDict = ReadFasta(jpnFasta)
for defline, seq in jpnDict.items():
    strain = defline.split("|")[0]
    
    #grab info from metadata dictionary
    if len(jpnMetaDict[strain]) == 1:
        subtype = jpnMetaDict[strain][0][0]; date = jpnMetaDict[strain][0][1]
        cntry = jpnMetaDict[strain][0][2]; host = jpnMetaDict[strain][0][3]
    else:
        print("ERROR 5!")
        sys.exit()
        
    #test for defline duplicates
    if len(seq) != 1:
        print("ERROR 5-2!")
        sys.exit()
        
    #output
    newlines = ">offlu-vcm|%s|%s|%s|%s||%s\n%s\n" % (strain, subtype, host, cntry, date, seq[0])
    mainFasta.write(newlines)
    
    
synDict = ReadFasta(synFasta)
for defline, seq in synDict.items():
    defLst = defline.strip().split("|")
    strain = defLst[1]
    subtype = defLst[2]
    host = "Swine"
    cntry = defLst[4]
    date = defLst[-1].strip("-variant-clade")
        
    #test for defline duplicates
    if len(seq) != 1:
        print("ERROR 6!")
        sys.exit()
    
    #output
    newlines = ">syntheticIAV|%s|%s|%s|%s||%s\n%s\n" % (strain, subtype, host, cntry, date, seq[0])
    mainFasta.write(newlines)










ukFasta.close(); ukMeta.close(); belFasta.close(); belMeta.close()
canFasta.close(); canMeta.close(); itaFasta.close(); itaMeta.close()
umnFasta.close(); jpnFasta.close(); jpnMeta.close(); synFasta.close()
mainFasta.close()








