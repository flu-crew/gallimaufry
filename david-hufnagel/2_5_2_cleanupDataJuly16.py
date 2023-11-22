#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A seq is designed to remove A/PIGEON/Hunan/185/2010, removing defline 
duplicates, and modify misspellings in strain names
Created by David E. Hufnagel on Fri Jul 16 15:19:40 2021
"""
import sys
inpH1 = open("mergedSeqs_v5_h1.fna")
inpH3 = open("mergedSeqs_v5_h3.fna")
outH1 = open("mergedSeqs_v5_h1_strainClean.fna", "w")
outH3 = open("mergedSeqs_v5_h3_strainClean.fna", "w")
dupsH1 = open("dupsJuly16_H1.fna", "w")





def SaveIntoDict(key, val, dictx):
    if key in dictx:
        dictx[key].append(val)
    else:
        dictx[key] = [val,]
        
def ReadFasta(fd): #Go through input and store the file in a dict of key: defline   val: seq
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





#Go through H1 input, cleanup strains, remove A/PIGEON/Hunan/185/2010, and output the result
h1Dict = ReadFasta(inpH1)
dupID = 1
for defline, seq in h1Dict.items():
    if len(seq) == 1:
        defLst= defline.split("|")
        strain = defLst[-6]
        if not strain in ["A/PIGEON/Hunan/185/2010","A/swine/Gunma/7-3732/2016", "A/swine/Gunma/34-6730/2019", "A/swine/Gunma/36-6894/2019"]:
            if strain.count("/") == 1:
                pass  #these are unusual, but fine
            elif strain.count("/") == 3:
                pass  #everything seems right here
            elif strain.count("/") == 4:
                if "North_Caroloina" in strain:
                    strain = strain.replace("North_Caroloina","North_Carolina")
            elif strain.count("/") == 5:
                pass  #everything seems right here
            else:
                print("ERROR 1!")
                sys.exit()
                
            defLst[-6] = strain
            newDef = "|".join(defLst)
            newlines = ">%s\n%s\n" % (newDef, seq[0])
            outH1.write(newlines)
    else:
        if len(seq) == 2:
            newlines = ">%s__%s\n%s\n" % (defline, dupID, seq[0])
            dupsH1.write(newlines)
            dupID += 1
            newlines = ">%s__%s\n%s\n" % (defline, dupID, seq[1])
            dupsH1.write(newlines)
            dupID += 1
        else:
            print("ERROR 4!")
            sys.exit()


#Go through H3 input, cleanup strains and output the result
h3Dict = ReadFasta(inpH3)
for defline, seq in h3Dict.items():
    if len(seq) == 1:
        strain = defline.split("|")[-6]
        if strain.count("/") == 2:
            pass #everything seems right here
        elif strain.count("/") == 3:
            pass #everything seems right here
        elif strain.count("/") == 4:
            pass #everything seems right here
        elif strain.count("/") == 5:
            pass #everything seems right here
        else:
            print("ERROR 2!")
            sys.exit()

        newlines = ">%s\n%s\n" % (defline, seq[0])
        outH3.write(newlines)
    else:
        print("ERROR 3!")
        sys.exit()






inpH1.close()
inpH3.close()
outH1.close()
outH3.close()
dupsH1.close()