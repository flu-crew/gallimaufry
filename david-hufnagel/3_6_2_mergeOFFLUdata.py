#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script creates the first merged OFFLU fasta file for the Sept 2022 
season using all currently available data
Created by David E. Hufnagel on Jul 11, 2022
"""
import sys

#Open input and output files
italyMeta = open("Italy1-2022_VCM_data_template_SI.csv")
japanMeta = open("VCM_data_SI_NIAHJapan.csv")
oldH1 = open("mergedSeqs_h1_v22.fna")
oldH3 = open("mergedSeqs_h3_v22.fna")
newPrivateH1 = open("offlu-vcm-H1_wClass.fasta")
newPrivateH3 = open("offlu-vcm-H3_wClass.fasta")
newPublicH1 = open("public-h1_wClass.fasta")
newPublicH3 = open("public-h3_wClass.fasta")
outH1 = open("mergedData_h1_v1.fna", "w")
outH3 = open("mergedData_h3_v1.fna", "w")





#Define functions
def ProcessMeta(fd):
    metaDict = {}
    fd.readline()
    for line in fd:
        lineLst = line.strip().split(",")
        subtype = lineLst[3]
        date = lineLst[4]
        strain = lineLst[0]
        
        strainLst = strain.split("/")
        if len(strainLst) == 6:
            strain = "/".join(strainLst[:-1])
        
        if "/" in date:
            dateLst = date.split("/")
            newDate = "20" + "-".join([dateLst[2],dateLst[0],dateLst[1]])
            date = newDate
            
        metaDict[strain] = (subtype, date)
    
    return(metaDict)


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


def ProcessOld(fd, out):
    fastaDict = ReadFasta(fd)
    for defline, seqs in fastaDict.items():
        if len(seqs) > 1:
            print("ERROR1!")
            sys.exit()
        elif "onsensus" not in defline:
            seq = seqs[0]
            defLst = defline.split("|")
            prov = defLst[0]
            if prov in ["CVV","SwReference","huReference","huVaccine","variant"] or 'lab-' in defline:
                defLst[0] = defLst[0].replace("SwReference","swReference")
                defLst.insert(7,"")
                newDef = "|".join(defLst)
                newlines = ">%s\n%s\n" % (newDef, seq)
                out.write(newlines)
                
                
def ProcessPrivate(fd, out, itaDict, japDict):
    fastaDict = ReadFasta(fd)
    for defline, seqs in fastaDict.items():
        if len(seqs) > 1:
            print("ERROR2!")
            sys.exit()
        else:
            seq = seqs[0]
            defLst = defline.split("|")
            strain = defLst[0].split("(")[0]
            clade = defLst[1]
            
            strainLst = strain.split("/")
            if len(strainLst) == 6:
                strain = "/".join(strainLst[:-1])
            
            if strain in itaDict:
                subtype = itaDict[strain][0]
                date = itaDict[strain][1]
                cntry = "ITA"
            elif strain in japDict:
                subtype = japDict[strain][0]
                date = japDict[strain][1]
                cntry = "JAP"
            elif "_iav" in strain:
                cntry = "USA" #there is no metadata for ISU strains at this time
            else:
                print("ERROR3!")
                print(strain)
                sys.exit()
              
            newDef = "offlu-vcm||||||||%s|%s|Swine|%s|%s|%s" % (strain,subtype,cntry,clade,date)
            newlines = ">%s\n%s\n" % (newDef, seq)
            out.write(newlines)
            
            
def ProcessPublic(fd,out):
    fastaDict = ReadFasta(fd)
    for defline, seqs in fastaDict.items():
        #This section was removed due to A/swine/Indiana/A01812320_HA/2022 which shows up twice with exactly the same sequence
        # if len(seqs) > 1:
        #     print("ERROR4!")
        #     print(defline)
        #     #sys.exit()
        seq = seqs[0]
        defLst = defline.strip().split("|")
        strain = defLst[0]
        subtype = defLst[1].replace("N?","")
        cntry = defLst[3]
        clade = defLst[4]
        date = defLst[5]

        newDef = "publicIAV||||||||%s|%s|Swine|%s|%s|%s" % (strain,subtype,cntry,clade,date)
        newlines = ">%s\n%s\n" % (newDef, seq)
        out.write(newlines)



#####   BODY   #####
#Go through metadata files and make dicts of key: strain name val: (subtype, date)
italyMetaDict = ProcessMeta(italyMeta)
japanMetaDict = ProcessMeta(japanMeta)


#Go through old fastas, identify references, and output them
ProcessOld(oldH1, outH1)
ProcessOld(oldH3, outH3)


#Go through private sequences, reformat, and output them all
ProcessPrivate(newPrivateH1, outH1, italyMetaDict, japanMetaDict)
ProcessPrivate(newPrivateH3, outH3, italyMetaDict, japanMetaDict)


#Go through public sequences, reformat, and output them all
ProcessPublic(newPublicH1,outH1)
ProcessPublic(newPublicH3,outH3)











italyMeta.close()
japanMeta.close()
oldH1.close()
oldH3.close()
newPrivateH1.close()
newPrivateH3.close()
newPublicH1.close()
newPublicH3.close()
outH1.close()
outH3.close()






