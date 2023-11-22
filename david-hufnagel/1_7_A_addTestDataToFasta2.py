#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take an excel file containing information on 
strains that have been HI tested in current or previous OFFLU reports and
add that information to the most updated fasta files
Created by David E. Hufnagel on Wed Feb  3 10:41:40 2021
Updated by David E. Hufnagel on Feb 23, 2021
This version includes homologous strains, CVVs, variants and vaccines for a
more complete account of HI test data.
"""
import sys
hiDataFD = open("PrevTestTable2.txt")
h1Inp = open("h1.fna")
h3Inp = open("h3.fna")
h1Inp2019 = open("Z_oldData/1_2019b/allH1.fasta")
h3Inp2019 = open("Z_oldData/1_2019b/H3_subset_formatted.fna")
h1Inp2020a = open("Z_oldData/2_2020a/H1-combine.fasta")
h3Inp2020a = open("Z_oldData/2_2020a/H3_new.fna")
h1Inp2020b = open("Z_oldData/3_2020b/h1.fna")
h3Inp2020b = open("Z_oldData/3_2020b/h3.fna")
ohFasta = open("ohio32.fna")
h1Out = open("h1_wHI.fna", "w")
h3Out = open("h3_wHI.fna", "w")



def MakeHIStr(chunk):
    newStr = ""
    cnt = 1
    for x in chunk:
        if x != "N":
            if cnt == 1:
                newStr += "lab-19-b"
            elif cnt == 2:
                newStr += "lab-20-a"
            elif cnt == 3:
                newStr += "lab-20-b"
            elif cnt == 4:
                newStr += "lab-21-a"
        newStr += "|"
        
        cnt += 1
    newStr = newStr[:-1]
        
    return(newStr)

def ProcessFasta(inp, out, listx):
    for line in inp:
        if line.startswith(">"):
            if "Consensus" not in line:
                lineLst = line.strip().strip(">").split("|")
                strain = lineLst[2]

                if strain in listx:
                    listx.remove(strain)
                if strain in hiDataDict:
                    lineLst[1] = hiDataDict[strain]
                else:
                    lineLst[1] = "|||"
                    
                newline = ">%s\n" % ("|".join(lineLst))
                out.write(newline)
            else:
                out.write(line)
        else:
            out.write(line)
            
            
def ProcessOldFasta(inp, out, listx):
    toKeep = False
    for line in inp:
        if line.startswith(">"):
            if "Consensus" not in line:
                lineLst = line.strip().strip(">").split("|")
                
                #these files have internally inconsistent formats so here's how I try to get the right strain name regardless
                strain = lineLst[1]
                if not strain.startswith("A"):
                    strain = lineLst[0]
                    if not strain.startswith("A"):
                        strain = lineLst[2]
                        if not strain.startswith("A"):
                            strain = lineLst[3]
                if "/" not in strain:
                    strain = strain.replace("_","/")
                        
                if strain in listx:
                    toKeep = True
                    newline = ReformatOldDef(lineLst, strain)
                    listx.remove(strain)
                    out.write(newline)
                else:
                    toKeep = False

        elif toKeep:
            out.write(line)
            
            
def ReformatOldDef(oldDefLst, strain):
    host = "Swine"; clade = ""; cntry = ""; date = ""
    
    if len(oldDefLst) == 7:
        subtype = oldDefLst[2].replace("Nx","")
        
        if oldDefLst[5][0] not in ["2","3"]:
            cntry = oldDefLst[5].replace("Belgium","BEL")
        else:
            date = oldDefLst[5]
            if not date.startswith("2"):
                date = "2018-01-31"                
            if oldDefLst[0].startswith("EPI_ISL"):
                cntry = "USA"
                
                
                
        if oldDefLst[3] == "Spain":
            cntry = "ESP"
        if oldDefLst[4].startswith("1")  or oldDefLst[4].startswith("3"):
            clade = oldDefLst[4]
        if oldDefLst[6].startswith("2"):
            date = oldDefLst[6]
        else:
            if oldDefLst[6].startswith("0"):
                date = "2018-06-02"
                
                
    elif len(oldDefLst) == 6:
        source = "publicIAV"
        strain = oldDefLst[1]
        subtype = oldDefLst[2].replace("v","")
        host = "Human"
        cntry = oldDefLst[4]
        date = oldDefLst[5]


    elif len(oldDefLst) == 5:   
        if not oldDefLst[0].startswith("A"):
            subtype = oldDefLst[2]
            
            cntry = oldDefLst[3]
            if cntry == "Belgium":
                cntry = "BEL"
            elif cntry.startswith("MN"):
                cntry = "USA"
            
            if cntry.startswith("1"):
                cntry = "USA"
                
            clade = oldDefLst[4]
            if clade.startswith("2"):
                date = clade
                clade = oldDefLst[3]
            else:
                date = ""

        else:  #process all seqs with the format that starts with strain
            subtype = oldDefLst[1].replace("Nx","")
            cntry = oldDefLst[2].replace("Belgium","BEL").replace("Spain","ESP")
            clade = oldDefLst[3]    
            
            if not "swine" in oldDefLst[0]:
                host = "Human"

        
    elif len(oldDefLst) == 4:
        if oldDefLst[0] == "KEEP":
            subtype = oldDefLst[2]; cntry = oldDefLst[3]
        else:
            subtype= oldDefLst[1].replace("Nx","") 
            cntry = oldDefLst[2]
            if cntry == "England":
                cntry = "GBR"
                clade = oldDefLst[3]
            elif cntry == "Belgium":
                cntry = "BEL"
                clade = oldDefLst[3]
            elif cntry == "Spain":
                cntry = "ESP"
                clade = oldDefLst[3]
            elif cntry == "Australia":
                cntry = "AUS"
                clade = ""
            elif cntry == "Switzerland":
                cntry = "CHE"
                clade = ""
            elif cntry == "USA":
                clade = oldDefLst[3]
            elif cntry.startswith("2"):
                cntry = "ITA"
                date = oldDefLst[2]
                clade = oldDefLst[3]
            elif cntry.startswith("1"):
                cntry = "ITA"
                date = oldDefLst[3]
                clade = oldDefLst[2]    
                
        if not ("swine" in oldDefLst[0] or "swine" in oldDefLst[1]) :
            host = "Human"
            

    elif len(oldDefLst) == 3:
        if oldDefLst[0].startswith("A"):
            subtype = oldDefLst[1]; date = oldDefLst[2]
            cntry = "ITA"
            if date == "USA":
                cntry = "USA"; date = strain.split("/")[-1]
        else:
            subtype = oldDefLst[2]
            cntry = "BRA"
            date = "1978"
                
        if not ("swine" in oldDefLst[0] or "swine" in oldDefLst[1]) :
            host = "Human"
            
        
    else:
        print("ERROR")
    
    
    if cntry == "":
        if strain.split("/")[2] == "Italy":
            cntry = "ITA"
        else:
            cntry = "USA"
    
    if date == "":
        date = strain.split("/")[-1]
        
    if clade != "":
        if clade[0] not in ["1","3"]:
            clade = ""
    
    if cntry == "Italy":
        cntry = "ITA"
    
    testData = hiDataDict[strain]
    source = sourceDict[strain]
    strain = strain.replace("Swine","swine").replace("pig","swine").replace("SW","swine").replace("Sw","swine")
    if "swineitzerland" in strain:
        strain = strain.replace("swineitzerland","Switzerland")
        
    newline = ">%s|%s|%s|%s|%s|%s|%s|%s\n" % (source, testData, strain, subtype, host, cntry, clade, date)    
    return(newline)

            




#Go through hiDataFD, generate a string representing lab HI data and store it
#  in a dict of key: strain  val: hiDataStr and a list of not yet used strains.
#  Also make a dict of key: strain  val: source
hiDataDict = {}
sourceDict = {}
hiDataFD.readline()
unusedStrains = []
for line in hiDataFD:
    lineLst = line.strip().split("\t")
    strain = lineLst[0]
    hiDataStr = MakeHIStr(lineLst[1:5])
    hiDataDict[strain] = hiDataStr
    
    unusedStrains.append(strain)
    
    if lineLst[7] == "Y":
        source = "publicIAV"
    elif lineLst[7] == "N":
        source = "offlu-vcm"
    else:
        print("ERROR!")
    sourceDict[strain] = source


#Go through h1 and h3, match strains with HI data, and output new data that 
#  includes HI test information.  Also removes strains from the list as
#  they're used to create an output
ProcessFasta(h1Inp, h1Out, unusedStrains)
ProcessFasta(h3Inp, h3Out, unusedStrains)


#Go through old fastas, match strains with HI data, and output new data that 
#  includes HI test information for all strains that remain in the list
ProcessOldFasta(h1Inp2020b, h1Out, unusedStrains)
ProcessOldFasta(h3Inp2020b, h3Out, unusedStrains)
ProcessOldFasta(h1Inp2020a, h1Out, unusedStrains)
ProcessOldFasta(h3Inp2020a, h3Out, unusedStrains)
ProcessOldFasta(h1Inp2019, h1Out, unusedStrains)
ProcessOldFasta(h3Inp2019, h3Out, unusedStrains)
ProcessOldFasta(ohFasta, h3Out, unusedStrains)


#This is how I check if all strains in the spreadsheet were used for the output
# print()
# print(unusedStrains)
# print(len(unusedStrains))





hiDataFD.close()
h1Inp.close()
h3Inp.close()
h1Inp2019.close()
h3Inp2019.close()
h1Inp2020a.close()
h3Inp2020a.close()
h1Inp2020b.close()
h3Inp2020b.close()
h1Out.close()
h3Out.close()