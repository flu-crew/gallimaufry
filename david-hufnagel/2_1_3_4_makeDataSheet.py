#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take a spreadsheet with information related to 
strains and a list of strains and merge them into a data sheet with only
strains of interest and needed information.
Created by David E. Hufnagel on Mon Mar 22 11:39:32 2021
"""
import sys

strainsFD = open("allStrains.txt")
dataFD = open("762352779734-allIRDassocData.txt")
out = open("strainMetaData_v3.txt", "w")





#Go through the data sheet and store all relavant data
dataDict = {}
dataFD.readline()
for line in dataFD:
    lineLst = line.strip().split("\t")
    strain = lineLst[0]; subtype = lineLst[1]; colDate = lineLst[2]; 
    cntry = lineLst[4]; state = lineLst[5]; passage = lineLst[7] 
    naAcc = lineLst[8]; ncbiID = lineLst[10]; usClade = lineLst[11]
    globClade = lineLst[12]
    #print(strain)
    newStrain = strain.replace("-","_").replace(" ","_").replace("swine","Swine").replace("SW","Swine")
    #print(newStrain)
    dataDict[newStrain] = (subtype, colDate, cntry, state, passage, \
                           naAcc, ncbiID, usClade, globClade)


#Output the title line
title = "strain\tsubtype\tcollection_date\tcountry\tUS_state\tUS_clade\tglobe_clade\tNA_accession\tNCBI_taxon_ID\thost\tpassage\n"
out.write(title)



#Go through strains, pair them with the rest of the data and create the output
for line in strainsFD:
    strain = line.strip()
    host = "Swine"; subtype = dataDict[strain][0]
    colDate = dataDict[strain][1]; cntry = dataDict[strain][2]
    state = dataDict[strain][3]; passage = dataDict[strain][4]
    naAcc = dataDict[strain][5]; ncbiID = dataDict[strain][6]
    usClade = dataDict[strain][7]; globClade = dataDict[strain][8]
    
    newline = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % \
        (strain, subtype, colDate, cntry, state, usClade, globClade, \
         naAcc, ncbiID, host, passage)
    newline = newline.replace("-N/A-","NA")#Use a more reasonable "NA"
    out.write(newline)






strainsFD.close()
dataFD.close()
out.close()