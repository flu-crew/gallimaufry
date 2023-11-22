#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to fix the dates on all sequences in this fasta file
using a 2-column file created by Zeb
Created by David E. Hufnagel on Aug 21, 2020
"""
import sys

fasta = open(sys.argv[1])
datesFd = open(sys.argv[2])
out = open(sys.argv[3], "w")



#Go through files containing dates and store them in a dict of key: strain val: date
datesDict = {}
for line in datesFd:
    lineLst = line.strip().split("\t")
    strain = lineLst[0].replace("'","_").replace(" ","_"); date = lineLst[1]
    datesDict[strain] = date

#Go through fasta, replace dates, and output the result
for line in fasta:
    if line.startswith(">"):
        lineLst = line.strip().strip(">").split("|")
        source = lineLst[0]
        if source == "publicIAV":
            strain = lineLst[1]
            strainDate = lineLst[1].split("/")[-1]
            oldDate = lineLst[-1]
            newDate = datesDict[strain]
            if oldDate != newDate:
                oldYear = oldDate.split("-")[0]
                newYear = newDate.split("-")[0]
                if strainDate == oldYear == newYear: #If both old and new dates match the strain date, just trust the old date
                    newLine = ">%s|%s\n" % ("|".join(lineLst[:-1]), oldDate)
                elif strainDate == oldYear: #If strain date matches only the old date, trust the old date
                    newLine = ">%s|%s\n" % ("|".join(lineLst[:-1]), oldDate)
                elif strainDate == newYear: #If strain date matches only the new date, trust the new date
                    newLine = ">%s|%s\n" % ("|".join(lineLst[:-1]), newDate)
                else:
                    print("ERROR!")
                    sys.exit()
                out.write(newLine)
            else:
                out.write(line)
        else:
            out.write(line)
    else:
        out.write(line)
        



fasta.close()
datesFd.close()
out.close()
