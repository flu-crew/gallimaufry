#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to return unpublished canadian data to the fasta and
also deal with swine viruses falsely labeled "humanVaccine" including stuff 
that wasn't properly date filtered
Created by David E. Hufnagel on Aug 5, 2020
"""
import sys
inpH1 = open("allH1data_dateFilt_ambigFilt_noDup_wClades_wCons_clean.fna")
inpH3 = open("allH3data_dateFilt_ambigFilt_noDup_wClades_wCons_clean.fna")
canadaH1 = open("CanadaSeqs/Canada_seqs_endlineFix_uniqueNames_HAnames_H1.fna")
canadaH3 = open("CanadaSeqs/Canada_seqs_endlineFix_uniqueNames_HAnames_H3.fna")
outH1 = open("allH1data_dateFilt_ambigFilt_noDup_wClades_wCons_clean2.fna", "w")
outH3 = open("allH3data_dateFilt_ambigFilt_noDup_wClades_wCons_clean2.fna", "w")



def ProcessCanada(fd, out):
    isGood = False
    lastDefline = ""
    lastSeq = ""
    for line in fd:
        if line.startswith(">"):
            lineLst = line.strip().split("_")
            source = "offlu"
            strain = "/".join(lineLst[0:5]).strip(">").replace("'","_").replace(" ","_")
            subtype = lineLst[7]
            host = "swine"
            date = lineLst[6]
            country = "Canada"
            defline = ">%s|%s|%s|%s|unknown|%s|%s" % (source, strain, subtype, host, country, date)
            year = int(date.split("-")[0])
            
            #Save info from last seq
            if isGood:
                newlines = "%s\n%s\n" % (lastDefline, lastSeq)
                out.write(newlines)
            
            if year >=2016:
                isGood = True
            else:
                isGood = False
            
            lastDefline = defline
            lastSeq = ""
        else:
            if isGood:
                lastSeq += line.strip()
                
    else:
        if isGood:
            newlines = "%s\n%s\n" % (lastDefline, lastSeq)
            out.write(newlines)
            
def ProcessBig(fd, out):
    for line in fd:
        if line.startswith(">"):
            if "consensus" in line:
                out.write(line)
            else:
                lineLst = line.strip().strip(">").split("|")
                source = lineLst[0]
                strain = lineLst[1]
                if source == "huVaccine" and strain.startswith("A/swine"):
                    newline = ">publicIAV|%s|%s|swine|unknown|%s|%s\n" % (lineLst[1], lineLst[2], lineLst[5], lineLst[6])
                    out.write(newline)
                else:
                    out.write(line)
        else:
            out.write(line)
                

#Canada H1
ProcessCanada(canadaH1, outH1)

#Canada H3
ProcessCanada(canadaH3, outH3)

#Big fasta H1
ProcessBig(inpH1, outH1)

#Big fasta H3
ProcessBig(inpH3, outH3)






inpH1.close()
inpH3.close()
canadaH1.close()
canadaH3.close()
outH1.close()
outH3.close()