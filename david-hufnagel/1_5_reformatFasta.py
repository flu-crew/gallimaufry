#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take a fasta file of N1 sequences, completely
reformats the deflines so that they fit our standards,  and removes empty lines.
standard format: source|strain|subtype|host|country|clade|date (YYYY-MM-DD)
*note the date format is not part of an established standard
Created by David E. Hufnagel on Fri Nov 19, 2020
"""
import sys

inp = open(sys.argv[1])      #allN1_Namerica.fasta
out = open(sys.argv[2], "w") #allN1s_v1.fna


def ReformatDate(oldDate):
        slashes = oldDate.count("/")
        
        if slashes == 2:   
            oldDateLst = oldDate.split("/")
            year = oldDateLst[2]; month = oldDateLst[0]; day = oldDateLst[1]
            newDate = "%s-%s-%s" % (year, month, day)
        elif slashes == 1:
            oldDateLst = oldDate.split("/")
            year = oldDateLst[1]; month = oldDateLst[0]
            newDate = "%s-%s" % (year, month)
        else:
            newDate = oldDate
            
        return(newDate)



for line in inp:
    if line.startswith(">"):
        lineLst = line.strip().strip(">").split("|")
        strain = lineLst[0]; subtype = lineLst[1]; host = "Swine" 
        country = lineLst[3]; clade = lineLst[4]
        date = ReformatDate(lineLst[-1])
        
        #Change A/SW and A/swine annotations to A/Swine
        strain = strain.replace("A/SW","A/swine").replace("Carollina","Carolina")
        
        newline = ">publicIAV|%s|%s|%s|%s|%s|%s\n" % \
            (strain, subtype, host, country, clade, date)
        out.write(newline)
    else:
        if line.strip() not in ["","\n","^M"]:
            out.write(line)



inp.close()
out.close()
