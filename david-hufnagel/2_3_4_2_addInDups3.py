#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to add chosen duplicate strains back into the main
fasta file.
Created by David E. Hufnagel on Wed Jun  2, 2021
#updated for fall 2021 OFFLU on July 14, 2021
"""

fasta = open("mergedSeqs_v1.fna")
dups = open("dups2_clean.fna")
out = open("mergedSeqs_v2.fna", "w")
CHOSEN = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, \
          38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, \
              72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100, \
                  102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122, 124, \
                      126, 128, 130, 132, 134, 136, 138, 140, 142, 144, 146, \
                          148, 150, 152, 154, 156, 158, 160, 162, 172]




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





#Read the fasta file and write it directly to the output
for line in fasta:
    out.write(line)

#Go through dups, choose the right sequences based on CHOSEN and output them
dupDict = ReadFasta(dups)
for defline, seq in dupDict.items():
    ID = int(defline.split("__")[-1])
    newDef = defline.split("__")[0]

    if len(seq) != 1:
        print("ERROR!")

    if ID in CHOSEN:
        newline = ">%s\n%s\n" % (newDef, seq[0])
        out.write(newline)







fasta.close()
dups.close()
out.close()