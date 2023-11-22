#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to merge several different fasta files with their
own formats into one big fasta file with one format:
source|strain|subtype|host|country|date
Created by David E. Hufnagel on Jul 13, 2020
"""
import sys

cvvH1 = open("CVVseqs/20190917_CDC_CVV_H1.fasta")
cvvH3 = open("CVVseqs/20190917_CDC_CVV_H3.fasta")
canadaH1 = open("CanadaSeqs/Canada_seqs_endlineFix_uniqueNames_HAnames_H1.fna")
canadaH3 = open("CanadaSeqs/Canada_seqs_endlineFix_uniqueNames_HAnames_H3.fna")
italy = open("ItalySeqs/Italy_seqs_HA.fna")
japan = open("JapanSeqs/Japan_seqs_raw.fna")
variantH1 = open("VariantSeqs/20190828_VariantCases_H1.fasta")
variantH3 = open("VariantSeqs/20190828_VariantCases_H3.fasta")
humanVacH1 = open("humanVaccineSeqs/humanVacc_seqs_H1.fna")
humanVacH3 = open("humanVaccineSeqs/humanVacc_seqs_H3.fna")
ivr = open("ivrData_raw.fna")
outH1 = open("allH1data.fna", "w")
outH3 = open("allH3data.fna", "w")
italyDates = open("ItalySeqs/VCM_data_template_IZSLER_ITALY-2-2019-2020.txt")



#CVV H1
for line in cvvH1:
    if line.startswith(">"):
        lineLst = line.strip().split("|")
        source = "CVV"
        strain = lineLst[3]
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
        strain = lineLst[3]
        subtype = lineLst[4]
        host = "human"
        date = lineLst[7]
        country = "USA"
        
        newline = ">%s|%s|%s|%s|%s|%s\n" % (source, strain, subtype, host, country, date)
        outH3.write(newline)
    else:
        outH3.write(line)  


#Canada H1
for line in canadaH1:
    if line.startswith(">"):
        lineLst = line.strip().split("_")
        source = "offlu"
        strain = "/".join(lineLst[0:5]).strip(">")
        subtype = lineLst[7]
        host = "swine"
        date = lineLst[6]
        country = "Canada"
        
        newline = ">%s|%s|%s|%s|%s|%s\n" % (source, strain, subtype, host, country, date)
        outH1.write(newline)
    else:
        outH1.write(line)  


#Canada H3
for line in canadaH3:
    if line.startswith(">"):
        lineLst = line.strip().split("_")
        source = "offlu"
        strain = "/".join(lineLst[0:5]).strip(">")
        subtype = lineLst[7]
        host = "swine"
        date = lineLst[6]
        country = "Canada"
        
        newline = ">%s|%s|%s|%s|%s|%s\n" % (source, strain, subtype, host, country, date)
        outH3.write(newline)
    else:
        outH3.write(line)
        
#Italy dates
italyDateDict = {} #key: strain  val: date
italyDates.readline()
for line in italyDates:
    lineLst = line.strip().split("\t")
    date = lineLst[4]
    strain = "/".join(lineLst[0].split("_"))
    italyDateDict[strain] = date


#Italy sequences
for line in italy:
    if line.startswith(">"):
        lineLst = line.strip().split("_")
        source = "offlu"
        strain = "/".join(lineLst[0:-2]).strip(">")
        subtype = lineLst[-2]
        host = "swine"
        country = "Italy"
        date = italyDateDict[strain]        
        newline = ">%s|%s|%s|%s|%s|%s\n" % (source, strain, subtype, host, country, date)

        #determine whether this is an H1 or H3 strain 
        if subtype[:2] == "H1":
            outH1.write(newline)
            isH1 = True
            isH3 = False
        elif subtype[:2] == "H3":
            outH3.write(newline)
            isH1 = False
            isH3 = True
        else:
            print("ERROR!")
            sys.exit()
    else:
        if isH1:
            outH1.write(line)
        elif isH3:
            outH3.write(line) 
            
            
#Japan
for line in japan:
    if line.startswith(">"):
        lineLst = line.strip().split("|")
        source = "offlu"
        strain = lineLst[0].strip(">").split("_")[0]
        subtype = lineLst[0].split("_")[-1]
        host = "swine"
        country = "Japan"
        date = lineLst[1].split("@")[-1]     
        newline = ">%s|%s|%s|%s|%s|%s\n" % (source, strain, subtype, host, country, date)

        #determine whether this is an H1 or H3 strain 
        if subtype[:2] == "H1":
            outH1.write(newline)
            isH1 = True
            isH3 = False
        elif subtype[:2] == "H3":
            outH3.write(newline)
            isH1 = False
            isH3 = True
        else:
            print("ERROR!")
            sys.exit()
    else:
        if isH1:
            outH1.write(line)
        elif isH3:
            outH3.write(line)
            
            
#Variant H1
for line in variantH1:
    if line.startswith(">"):
        lineLst = line.strip().split("|")
        source = "variant"
        host = "human"
        if line.startswith(">A/Pavia"):
            strain = lineLst[0].strip(">")
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
        strain = lineLst[-5]
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
for line in humanVacH1:
    if line.startswith(">"):
        lineLst = line.strip().split("|")
        source = "huVaccine"
        host = "human"
        strain = lineLst[1]
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
        strain = lineLst[2]
                      
        subtype = lineLst[3]
        if line.startswith(">EPIIS"):
            strain = lineLst[1]
        else:
            strain = lineLst[2]

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



#IVR
for line in ivr:
    if line.startswith(">"):
        lineLst = line.strip().split("|")
        source = "IVR"
        strain = lineLst[1]
        subtype = lineLst[2]
        host = "swine"
        date = "-".join(lineLst[-3].split("/"))
        country = lineLst[-1]        
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
            print("ERROR!")
            print(subtype)
            sys.exit()
    else:
        if line != "\n":
            if isH1:
                outH1.write(line)
            elif isH3:
                outH3.write(line)




cvvH1.close()
cvvH3.close()
canadaH1.close()
canadaH3.close()
italy.close()
japan.close()
variantH1.close()
variantH3.close()
humanVacH1.close()
humanVacH3.close()
ivr.close()
outH1.close()
outH3.close()
italyDates.close()
