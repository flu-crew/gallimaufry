#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take OFFLU fastas and add in
previous test data from the last OFFLU report
Created by David E. Hufnagel on Wed Jul 21 11:04:04 2021
"""
import sys
springH1 = open("h1.fna")
springH3 = open("h3.fna")
inp1A = open("mergedSeqs_v9_h1_1A_wJPNclades_hostFix.fna")
inp1B = open("mergedSeqs_v9_h1_1B_fixHost.fna")
inp1C = open("mergedSeqs_v9_h1_1C_fixHost.fna")
inp3 = open("mergedSeqs_v9_h3_fixHost.fna")
out1A = open("mergedSeqs_v9_h1_1A_wJPNclades_hostFix_wPrevTest.fna", "w")
out1B = open("mergedSeqs_v9_h1_1B_fixHost_wPrevTest.fna", "w")
out1C = open("mergedSeqs_v9_h1_1C_fixHost_wPrevTest.fna", "w")
out3 = open("mergedSeqs_v9_h3_fixHost_wPrevTest.fna", "w")





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





#Go through last report's fastas and collect all strains that have been
#   previously HI tested and pipe them to the output 
springH1Dict = ReadFasta(springH1)
for defline, seq in springH1Dict.items():
    defLst = defline.split("|")
    testData = "".join(defLst[1:5])
    if testData:
        clade = defLst[-2]
        if len(seq) == 1:
            defLst.insert(5, "")
            newDef = "|".join(defLst)
            newlines = ">%s\n%s\n" % (newDef, seq[0])
            
            if clade.startswith("1A"):
                out1A.write(newlines)
            elif clade.startswith("1B"):
                out1B.write(newlines)
            elif clade.startswith("1C"):
                out1C.write(newlines)
            elif clade in [""]:
                pass
            else:
                print("ERROR2!")
                print(clade)
                sys.exit()
        else:
            if len(seq) == 2:
                newlinesA = ">%s\n%s\n" % (newDef, seq[0])  #don't worry about duplicates just yet, pass them along
                newlinesB = ">%s\n%s\n" % (newDef, seq[1])
                
                if clade.startswith("1C"):
                    out1C.write(newlinesA)
                    out1C.write(newlinesB)
                else:
                    print("ERROR 3!")
                    sys.exit()
            else:
                print("ERROR1!")
                print(defline)
                sys.exit()


springH3Dict = ReadFasta(springH3)
for defline, seq in springH3Dict.items():
    defLst = defline.split("|")
    testData = "".join(defLst[1:5])
    if testData:
        clade = defLst[-2]
        if len(seq) == 1:
            defLst.insert(5, "")
            newDef = "|".join(defLst)
            newlines = ">%s\n%s\n" % (newDef, seq[0])
            
            if clade.startswith("3.") or clade.startswith("Other-Human"):
                out3.write(newlines)
            elif clade in [""]:
                pass
            else:
                print("ERROR5!")
                print(clade)
                sys.exit()
        else:
            print("ERROR 4!")
            print(defline)
            sys.exit()


#Go through this report's fastas and output all data
inp1ADict = ReadFasta(inp1A)
for defline, seq in inp1ADict.items():
    if len(seq) == 1:
        newlines = ">%s\n%s\n" % (defline, seq[0])
        out1A.write(newlines)
    else:
        print("ERROR 6!")
        sys.exit()


inp1BDict = ReadFasta(inp1B)
for defline, seq in inp1BDict.items():
    if len(seq) == 1:
        newlines = ">%s\n%s\n" % (defline, seq[0])
        out1B.write(newlines)
    else:
        print("ERROR 7!")
        sys.exit()
        

inp1CDict = ReadFasta(inp1C)
for defline, seq in inp1CDict.items():
    if len(seq) == 1:
        newlines = ">%s\n%s\n" % (defline, seq[0])
        out1C.write(newlines)
    else:
        print("ERROR 8!")
        sys.exit()
        

inp3Dict = ReadFasta(inp3)
for defline, seq in inp3Dict.items():
    if len(seq) == 1:
        newlines = ">%s\n%s\n" % (defline, seq[0])
        out3.write(newlines)
    else:
        print("ERROR 9!")
        sys.exit()










springH1.close()
springH3.close()
inp1A.close()
inp1B.close()
inp1C.close()
inp3.close()
out1A.close()
out1B.close()
out1C.close()
out3.close()