#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Merges fasta files containing variants together in a smart way (gamma only, 
no duplicates, priority to newer files, standardized format)

Created by David E. Hufnagel on July 18, 2023
Update: Aug 17, 2023, this version is for Vaccines
Update: Aug 19, 2023, tis version is for all references with H3 files
"""
import sys

inp_20b = open("oflu2020b_h3_refs.fna")
inp_21a = open("oflu2021a_h3_refs.fna")
inp_21b = open("oflu2021b_h3_refs.fna")
inp_22a = open("oflu2022a_h3_refs.fna")
inp_22b = open("oflu2022b_h3_refs.fna")
inp_23a = open("oflu2023a_h3_refs.fna")
out = open("ofluh3_refs.fna", "w")



        
        
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
            print("ERROR1!")
            sys.exit()
        else:
            seq = seqs[0]
            defLst = defline.strip().split("|")
            prov = defLst[0]
            if len(defLst) > 5:
                strain = defLst[-6]
                sub = defLst[-5].replace("N1v","N1").replace("N2v","N2").replace("Nx","").replace("N0v","")
                cntry = defLst[-3]  #not all countries have 3-letter code
                clade = defLst[-2]
                date = defLst[-1]
                
                newdef = "%s|||||||||%s|%s|Human|%s|%s|%s" % (prov, strain, sub, cntry, clade, date)


            else:
                strain = defLst[1]
                if len(defLst) == 3:
                    newdef = "%s|||||||||%s||Human|USA||2020" % (prov, strain)
                elif len(defLst) == 5:
                    sub = defLst[-3].replace("v","")
                    cntry = defLst[-2]
                    clade = defLst[-1]
                    date = strain.split("/")[-1]

                    newdef = "%s|||||||||%s|%s|Human|%s|%s|%s" % (prov, strain, sub, cntry, clade, date)
                else:
                    print("ERROR2!")
                    sys.exit()
            newTup = (report, newdef, seq)
            SaveIntoDict(strain, newTup, keepDict)



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


