#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Merges fasta files containing variants together in a smart way (gamma only, 
no duplicates, priority to newer files, standardized format)

Created by David E. Hufnagel on July 18, 2023
Update: Aug 17, 2023, this version is for Vaccines
"""
import sys

inp_20b = open("offlu_2020b_h1_vac.fna")
inp_21a = open("offlu_2021a_h1_vac.fna")
inp_21b = open("offlu_2021b_h1_vac.fna")
inp_22a = open("offlu_2022a_h1_vac.fna")
inp_22b = open("offlu_2022b_h1_vac.fna")
inp_23a = open("offlu_2023a_h1_vac.fna")
out = open("offlu_h1_vac.fna", "w")



        
        
def SaveIntoDict(key, val, dictx):
    if key in dictx:
        dictx[key].append(val)
    else:
        dictx[key] = [val,]


def ReadFasta(fd): #Go through inp and store the file in a dict of key: defline   val: seq
    fastaDict = {}
    oldDef = ""; oldSeq = ""
    for line in fd:
        if line.startswith(">"):
            if oldSeq != "":
                SaveIntoDict(oldDef, oldSeq, fastaDict)
                oldDef = line.strip().strip(">")
                oldSeq = ""
            else:
                oldDef = line.strip().strip(">")
        else:
            oldSeq += line.strip()
    else:
        SaveIntoDict(oldDef, oldSeq, fastaDict)
        
    return(fastaDict)


def ProcessFasta(fd, report):
    inpDict = ReadFasta(fd)
    for defline, seqs in inpDict.items():
        if len(seqs) > 1:
            print("ERROR!")
            sys.exit()
        else:
            seq = seqs[0]
            defLst = defline.strip().split("|")
            if len(defLst) > 3:
                print(defLst)
                strain = defLst[-6]
                sub = defLst[-5].replace("N1v","N1").replace("N2v","N2").replace("Nx","").replace("N0v","")
                cntry = defLst[-3]  #not all countries have 3-letter code
                clade = defLst[-2]
                
                if cntry in ["human","1C.2.2"]:
                    cntry = defLst[-2]
                    clade = defLst[-3]
                if clade == "human":
                    clade = ""
                date = defLst[-1].replace("__1","")
                if clade in ["","1A.3.3.3"]:
                    newdef = "huVaccine|%s|%s|Human|%s|%s|%s" % (strain, sub, cntry, clade, date)
                    newTup = (report, newdef, seq)
                    SaveIntoDict(strain, newTup, keepDict)
                    
                print(defline)
                print(strain)



#Go through fastas starting with the newest, make a dict of key: strain  
#  val: (report, newdef, seq) and a list of strains. Add only
#  gamma and unknown clade strains.
keepDict = {}
ProcessFasta(inp_23a,"23a")
ProcessFasta(inp_22b,"22b")
ProcessFasta(inp_22a,"22a")
ProcessFasta(inp_21b,"21b")
ProcessFasta(inp_21a,"21a")
ProcessFasta(inp_20b,"20b")


#Go through the dict, and combine all strain clusters containing all OFFLU
#  information into one defline, seq combo per strain, output to a combined, 
#  formatted, gamma-only, no-duplicate fasta.  ##### After looking at the data
#  decided to keep the newest
for strain, tup in keepDict.items():
    newdef = tup[0][1]
    seq = tup[0][2]
    newlines = ">%s\n%s\n" % (newdef,seq)
    out.write(newlines)





inp_20b.close()
inp_21a.close()
inp_21b.close()
inp_22a.close()
inp_22b.close()
inp_23a.close()
out.close()


