#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to merge several different fasta files with their
own formats into one big fasta file with one format:
source|strain|subtype|host|country|date
This version is for public data only, which was given to me by Zeb and includes
clades and 2 new human vaccines
Created by David E. Hufnagel on Jul 28, 2020
"""
import sys

cvvH1 = open("CVVseqs/20190917_CDC_CVV_H1.fasta")
cvvH3 = open("CVVseqs/20190917_CDC_CVV_H3.fasta")
variantH1 = open("VariantSeqs/20190828_VariantCases_H1.fasta")
variantH3 = open("VariantSeqs/20190828_VariantCases_H3.fasta")
humanVacH1 = open("humanVaccineSeqs/humanVacc_seqs_H1.fna")
humanVacH3 = open("humanVaccineSeqs/humanVacc_seqs_H3.fna")
zeb = open("global_all-HA_v2.fasta")
aliciaData = open("2020_IAVS_list.txt")
aliciaFasta = open("aliciaSeqs2020.fna")
outH1 = open("allH1data.fna", "w")
outH3 = open("allH3data.fna", "w")



#CVV H1
for line in cvvH1:
    if line.startswith(">"):
        lineLst = line.strip().split("|")
        source = "CVV"
        strain = lineLst[3].replace(" ","_")
        subtype = lineLst[4]
        host = "human"
        date = lineLst[7]
        if "Hunan" in strain:
            country = "China"
        elif "Netherlands" in strain:
            country = "Netherlands"
        else:
            country = "USA"
        
        newline = ">%s|%s|%s|%s|%s|%s\n" % (source, strain, subtype, host, country, date)
        outH1.write(newline)
    else:
        outH1.write(line)


#CVV H3
for line in cvvH3:
    if line.startswith(">"):
        lineLst = line.strip().split("|")
        source = "CVV"
        strain = lineLst[3].replace(" ","_")
        subtype = lineLst[4]
        host = "human"
        date = lineLst[7]
        country = "USA"
        
        newline = ">%s|%s|%s|%s|%s|%s\n" % (source, strain, subtype, host, country, date)
        outH3.write(newline)
    else:
        outH3.write(line)  
            
            
#Variant H1
for line in variantH1:
    if line.startswith(">"):
        lineLst = line.strip().split("|")
        source = "variant"
        host = "human"
        if line.startswith(">A/Pavia"):
            strain = lineLst[0].strip(">").replace(" ","_")
            subtype = lineLst[1]
            country = lineLst[2]
            date = "2016"
        else:
            strain = lineLst[-5]
            subtype = lineLst[-4]
            date = lineLst[-1]
            if "Parana" in strain:
                country = "Brazil"
            elif "Tianjin-baodi" in strain:
                country = "China"
            else:
                country = "USA"
                
        newline = ">%s|%s|%s|%s|%s|%s\n" % (source, strain, subtype, host, country, date)
        outH1.write(newline)
    else:
        outH1.write(line)
        
        
#Variant H3
for line in variantH3:
    if line.startswith(">"):
        lineLst = line.strip().split("|")
        source = "variant"
        host = "human"
        strain = lineLst[-5].replace(" ","_")
        subtype = lineLst[-4]
        date = lineLst[-1]
        if "South_Australia" in strain:
            country = "Australia"
        else:
            country = "USA"
                
        newline = ">%s|%s|%s|%s|%s|%s\n" % (source, strain, subtype, host, country, date)
        outH3.write(newline)
    else:
        outH3.write(line)
outH1.write("\n")  #This prevents the next line starting without an endline


#Human vaccine H1
vacIncluded = [] #already included vaccine strains
for line in humanVacH1:
    if line.startswith(">"):
        lineLst = line.strip().split("|")
        source = "huVaccine"
        host = "human"
        strain = lineLst[1].replace(" ","_")
        vacIncluded.append(strain)
        subtype = lineLst[2]
        if line.startswith(">EPIIS"):
            date = lineLst[3]
        else:
            date = strain.split("/")[-1]

        if "Guangdong-Maonan" in strain or "Beijing" in strain:
            country = "China"
        elif "Bayern" in strain:
            country = "Germany"
        elif "New_Caledonia" in strain:
            country = "France_New_Caledonia"
        elif "Solomon_Islands" in strain:
            country = "Solomon_Islands"
        elif "Brisbane" in strain:
            country = "Australia"
        elif "USSR" in strain:
            country = "USSR"
        elif "Brazil" in strain:
            country = "Brazil"
        elif "Chile" in strain:
            country = "Chile"
        elif "Taiwan" in strain:
            country = "Taiwan"
        elif "Singapore" in strain:
            country = "Singapore"
        else:
            country = "USA"

        newline = ">%s|%s|%s|%s|%s|%s\n" % (source, strain, subtype, host, country, date)
        outH1.write(newline)
    else:
        outH1.write(line)


#Human vaccine H3
for line in humanVacH3:
    if line.startswith(">"):
        lineLst = line.strip().split("|")
        source = "huVaccine"
        host = "human"
        strain = lineLst[2].replace(" ","_")
                      
        subtype = lineLst[3]
        if line.startswith(">EPIIS"):
            strain = lineLst[1].replace(" ","_")
        else:
            strain = lineLst[2].replace(" ","_")

        date = strain.split("/")[-1]    
        

        if "Guangdong-Maonan" in strain or "Beijing" in strain or "Sichuan" \
            in strain or "Shanghai" in strain or "Guizhou" in strain or \
                "Shangdong" in strain or "Wuhan" in strain or "Nanchang" in \
                    strain or "Fujian" in strain:
            country = "China"
        elif "Hong_Kong" in strain:
            country = "Hong_Kong"
        elif "Port_Chalmers" in strain or "Wellington" in strain:
            country = "New Zealand"
        elif "Victoria" in strain or "Sydney" in strain or "Brisbane" in \
            strain or "Perth" in strain or "Australia" in strain:
            country = "Australia"
        elif "Bangkok" in strain:
            country = "Thailand"
        elif "Philippines" in strain:
            country = "Philippines"
        elif "Leningrad" in strain:
            country = "USSR"
        elif "Johannesburg" in strain:
            country = "South Africa"
        elif "Moscow" in strain:
            country = "Russia"
        elif "Panama" in strain:
            country = "Panama"
        elif "KUMAMOTO" in strain or "Hiroshima" in strain:
            country = "Japan"
        elif "Uruguay" in strain:
            country = "Uruguay"
        elif "Switzerland" in strain:
            country = "Switzerland"
        elif "Norway" in strain:
            country = "Norway"
        elif "Stockholm" in strain:
            country = "Sweden"
        elif "Singapore" in strain:
            country = "Singapore"
        else:
            country = "USA"

        newline = ">%s|%s|%s|%s|%s|%s\n" % (source, strain, subtype, host, country, date)
        outH3.write(newline)
    else:
        outH3.write(line)
        

#Public data from Zeb including a couple human vaccines
for line in zeb:
    if line.startswith(">"):
        lineLst = line.strip().split("|")
        strain = lineLst[0].replace(" ","_").strip(">")
        subtype = lineLst[1]
        date = lineLst[-1]
        country = lineLst[-2]
        clade = lineLst[3]
        if clade == "humanVaccine":
            source = "huVaccine"
            host = "human"
        else:
            source = "publicIAV"
            host = "swine"
     
        newline = ">%s|%s|%s|%s|%s|%s\n" % (source, strain, subtype, host, country, date)

        #determine whether this is an H1 or H3 strain 
        if subtype[:2] == "H1":
            outH1.write(newline)
            isH1 = True
            isH3 = False
        elif subtype[:2] == "H3" or subtype == "mixed,H3":
            outH3.write(newline)
            isH1 = False
            isH3 = True
        else:
            errorLine = "%s was excluded as it is subtype '%s'\n" % (strain, subtype)
            isH1 = False
            isH3 = False
            print(errorLine)
    else:
        if line != "\n":
            if isH1:
                outH1.write(line)
            elif isH3:
                outH3.write(line)
                
#Store data for Alicia's seqs
aliciaDataDict = {} #key: strain  val: (subtype, date)
aliciaData.readline() 
for line in aliciaData:
    lineLst = line.strip().split("\t")
    strain = lineLst[1].split("(")[0].replace(" ","_")
    subtype = lineLst[1].split("(")[1].strip(")")
    date = lineLst[-2].split("/")
    newDate = "%s-%s-%s" % (date[2], date[0], date[1]) # reformat M D Y  -->  Y M D
    aliciaDataDict[strain] = (subtype, newDate)
    
#Process seqs from Alicia's data
isGood = False #whether to write seq to output
for line in aliciaFasta:
    if line.startswith(">"):
        strain = line.split("(")[1].replace(" ","_")
        source = "publicIAV"
        if strain in aliciaDataDict:
            subtype = aliciaDataDict[strain][0]
            date = aliciaDataDict[strain][1]
            host = "swine"
            country = "USA"
            
            newline = ">%s|%s|%s|%s|%s|%s\n" % (source, strain, subtype, host, country, date)
    
            #determine whether this is an H1 or H3 strain 
            if subtype[:2] == "H1":
                outH1.write(newline)
                isH1 = True
                isH3 = False
                isGood = True
            elif subtype[:2] == "H3" or subtype == "mixed,H3":
                outH3.write(newline)
                isH1 = False
                isH3 = True
                isGood = True
            else:
                errorLine = "%s was excluded as it is subtype '%s'\n" % (strain, subtype)
                isH1 = False
                isH3 = False
                isGood = False
                print(errorLine)
        else:
            isGood = False
    else:
        if line != "\n" and isGood:
            if isH1:
                outH1.write(line)
            elif isH3:
                outH3.write(line)
    
    








cvvH1.close()
cvvH3.close()
variantH1.close()
variantH3.close()
humanVacH1.close()
humanVacH3.close()
zeb.close()
outH1.close()
outH3.close()
aliciaData.close()
aliciaFasta.close()
