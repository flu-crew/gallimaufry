#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created by David E. Hufnagel on Tue Jan 26 16:58:12 2021
"""
import sys
microFD = open("Microreact_Master_List.txt")
h1FastaFD = open("h1_Jan25.fna")
h3FastaFD = open("h3_Jan25.fna")
out = open("microFastaCompareReport.txt", "w")



#Go through microFD and make a list of strain names present
microLst = []
microFD.readline()
for line in microFD:
    lineLst = line.strip().split("\t")
    strain = lineLst[1].replace("Swine", "swine").replace("/Sw/", "/swine/")
    microLst.append(strain)


#Go through h1FastaFD and make a list of strain names present
fastaLst = []
for line in h1FastaFD:
    if line.startswith(">"):
        if "Consensus" not in line:
            strain = line.split("|")[2].replace("Swine", "swine").replace("/Sw/", "/swine/")
            fastaLst.append(strain)


#Go through h3FastaFD and add strain names to the h1FastaFD list
for line in h3FastaFD:
    if line.startswith(">"):
        if "Consensus" not in line:
            strain = line.split("|")[2].replace("Swine", "swine").replace("/Sw/", "/swine/")
            fastaLst.append(strain)         


#Go through microLst and make a list of what is present in micro but not fastas
notFastas = []
for strain in microLst:
    if strain not in fastaLst:
        notFastas.append(strain)

#Go through fastaLst and make a list of what is present in fastas but not micro
notMicro = []
for strain in fastaLst:
    if strain not in microLst:
        notMicro.append(strain)

#Output data 
newline = "These seqs are in microreact table, but not in fastas (%s total):\n" % (len(notFastas))
out.write(newline)
for strain in notFastas:
    newline = "%s\n" % (strain)
    out.write(newline)
    
newline = "These seqs are in fastas, but not in microcreact table (%s total):\n" % (len(notMicro))
out.write(newline)
for strain in notMicro:
    newline = "%s\n" % (strain)
    out.write(newline)





microFD.close()
h1FastaFD.close()
h3FastaFD.close()
out.close()