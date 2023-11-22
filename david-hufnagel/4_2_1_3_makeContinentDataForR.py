#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script takes a fasta file for the combined N. American and global data
and makes a csv data file to be processed by R for the purpose of
plotting the continents represented in clades
Created by David E. Hufnagel on Feb  2, 2023
"""
import sys

inp = open(sys.argv[1])
out = open(sys.argv[2], 'w')





def GetContinent(cntry):
    if cntry in ["Canada", "USA", "Mexico","Costa_Rica","Guatemala","Cuba"]:
        return("N. America")
    elif cntry in ["France", "Germany","Netherlands","Italy","Belgium",\
                   "Sweden","United_Kingdom","Denmark","Ireland","Poland", \
                       "Czech_Republic", "Spain", "Hungary", "Norway", "Russia",\
                           "Finland","Serbia"]:
        return("Europe")
    elif cntry in ["China", "Japan","Hong_Kong","Taiwan","Thailand", "South_Korea", \
                   "Indonesia","India","Sri_Lanka","Israel","Singapore","Portugal",\
                       "Myanmar","Kazakhstan"]:
        return("Asia")
    elif cntry in ["Argentina","Peru","Brazil","Colombia","Chile"]:
        return("S. America")
    elif cntry in ["Australia"]:
        return("Oceania")
    elif cntry in ["Nigeria","Kenya","Togo","Zambia"]:
        return("Africa")
    else:
        print("ERROR: country not defined!")
        print(cntry)
        sys.exit()
    
    
    
#BODY
title = "strain,clade,continent\n"
out.write(title)
for line in inp:
    if line.startswith(">"):
        lineLst = line.strip().strip(">").split("|")
        strain = lineLst[1]
        clade = lineLst[5]
        cont = GetContinent(lineLst[4])
        newline = "%s,%s,%s\n" % (strain, clade, cont)
        out.write(newline)











inp.close()
out.close()