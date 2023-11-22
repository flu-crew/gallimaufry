#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to merge the H1 data file sent to us by the RVC of
unpublished data with our current public H1 data under a sigle format:
source|strain|subtype|host|clade|country|date
Created by David E. Hufnagel on Aug  7, 2020
"""
import sys
rvcFd = open("h1-unpublished.fasta")
usdaFd = open("allH1data_dateFilt_ambigFilt_noDup_wClades_wCons_clean2.fna")
out = open("allH1data_rvc_usda.fna","w")


#determine country from strain name
def GetCountry(strain):
    if "Italy" in strain or "PAVIA" in strain:
        country = "ITA"
    elif "England" in strain:
        country = "GBR"
    elif "Belgium" in strain or "BELGIUM" in strain or "Gent" in strain:
        country = "BEL"
    elif "Ontario" in strain or "Quebec" in strain:
        country = "CAN"
    elif "France" in strain:
        country = "FRA"
    elif "Gunma" in strain or "Okayama" in strain:
        country = "JPN"
    elif "Brazil" in strain:
        country = "BRA"
    elif "Korea" in strain:
        country = "KOR"
    elif "Spain" in strain or "SPAIN" in strain:
        country = "ESP"
    elif "NETHERLANDS" in strain or "Netherlands" in strain:
        country = "NLD"
    elif "Germany" in strain:
        country = "DEU"
    elif "Denmark" in strain:
        country = "DNK"
    elif "Ireland" in strain:
        country= "IRL"
    else:
        print("WARNING")
        country = "NA"
        
    return(country)

#determine date from strain name
def GetDate(strain):
    date = strain.split("/")[-1]
    if len(date) != 4:
        print(date)
    
    return(date)

def GetSubtype(clade):
    if clade.startswith("1"):
        return ("H1")
    elif clade.startswith("3"):
        return ("H3")
    else:
        print("ERROR4")
        print(clade)
        sys.exit()
    
    


#Go through usda data and output it as is
for line in usdaFd:
    out.write(line)


#Go through rvc data, reformat it and output it 
for line in rvcFd:
    if line.startswith(">"):
        lineLst = line.strip().strip(">").split("|")
        source = "offlu"; subtype = "NA"; clade = "NA"; country = "NA"; date = "NA"
        if line.startswith(">OFFLU"):
            strain = lineLst[1]; subtype = lineLst[2]; host = "swine"
            if len(lineLst) == 5:
                clade = lineLst[3]; date = lineLst[4]
            elif len(lineLst) == 4:
                clade = lineLst[3]
                date = GetDate(strain)
            elif len(lineLst) == 3:
                date = GetDate(strain)
            else:
                print("ERROR2!")
                print(line)
                sys.exit()
            
            country = GetCountry(strain)
            
        elif line.startswith(">collab|forHI"):
            strain = lineLst[2]; host = "swine"
            if len(lineLst) == 6:
                subtype = lineLst[3]
                country = lineLst[4]
                clade = lineLst[5]
                date = GetDate(strain)
            elif len(lineLst) == 5:
                if "England" in strain:
                    subtype = lineLst[3]
                    clade = lineLst[4]   
                    country = GetCountry(strain)
                    date = GetDate(strain)
                    subtype = GetSubtype(clade)
                else:
                    clade = lineLst[3]
                    date = lineLst[4]
                    country = GetCountry(strain)
                    subtype = GetSubtype(clade)

            else:
                print("ERROR3!")
                sys.exit()
        
        elif line.startswith(">collab|variant"):
            strain = lineLst[4]
            host = "human"
            clade = lineLst[5]
            subtype = GetSubtype(clade)
            country = GetCountry(strain)
            date = GetDate(strain)
        
        elif line.startswith(">forHI"):
            host = "swine"
            if len(lineLst) == 5:
                strain = lineLst[1]
                subtype = lineLst[2]
                clade = lineLst[3]
                date = lineLst[4]
            elif len(lineLst) == 4:
                strain = lineLst[2]
                clade = lineLst[3]
                date = GetDate(strain)
                subtype = GetSubtype(clade)
            elif len(lineLst) == 3:
                strain = lineLst[1]
                clade = lineLst[2]
                date = GetDate(strain)
                subtype = GetSubtype(clade)
            else:
                print("ERROR5!")
                sys.exit()
            country = GetCountry(strain)
            
        else:
            print("ERROR1!")
            sys.exit()
            
        newline = ">%s|%s|%s|%s|%s|%s|%s\n" % (source, strain, subtype, host, clade, country, date)
        out.write(newline)
    else:
        out.write(line)





rvcFd.close()
usdaFd.close()
out.close()