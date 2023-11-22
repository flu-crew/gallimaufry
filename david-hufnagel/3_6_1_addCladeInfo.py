#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to add clade information into unformatted private 
offlu sequences and semi-formatted public sequences
Created by David E. Hufnagel on Jul  8, 2022
"""
import sys


publicH1 = open("public-h1.fasta")
publicH3 = open("public-h3.fasta")
cladePubH1 = open("public.classification.H1-v1")
cladePubH3 = open("public.classification.H3-v1")
privateH1 = open("offlu-vcm-H1.fasta")
privateH3 = open("offlu-vcm-H3.fasta")
cladePrivH1 = open("offlu.classification.H1-v1")
cladePrivH3 = open("offlu.classification.H3-v1")
publicH1Out = open("public-h1_wClass.fasta", "w")
publicH3Out = open("public-h3_wClass.fasta", "w")
privateH1Out = open("offlu-vcm-H1_wClass.fasta", "w")
privateH3Out = open("offlu-vcm-H3_wClass.fasta", "w")





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


def ProcessClassif(fd):
    classDict = {}
    for line in fd:
        lineLst = line.strip().split("\t")
        classDict[lineLst[0]] = lineLst[1]
        
    return(classDict)


def AddClassPub(fd, classDict, out):
    fastaDict = ReadFasta(fd)
    
    for defline, seqs in fastaDict.items():
        if len(seqs) > 1:
            print("ERROR1")
            sys.exit()
        else:
            defLst = defline.strip().split("|")
            defLst[-2] = classDict[defline]

            newDef = "|".join(defLst)
            newlines = ">%s\n%s\n" % (newDef, seqs[0])
            out.write(newlines)


def AddClassPriv(fd, classDict, out):
    fastaDict = ReadFasta(fd)
    
    for defline, seqs in fastaDict.items():
        if len(seqs) > 1:
            print("ERROR2")
            sys.exit()
        else:
            clade = classDict[defline]
            newlines = ">%s|%s\n%s\n" % (defline.strip(), clade, seqs[0])
            out.write(newlines)





#Go through classification files and make dicts of key: defline val: clade
classDict_publicH1 = ProcessClassif(cladePubH1)
classDict_publicH3 = ProcessClassif(cladePubH3)
classDict_privateH1 = ProcessClassif(cladePrivH1)
classDict_privateH3 = ProcessClassif(cladePrivH3)


#Go through public fastas and replace clade field with clades from 
#  classification files
AddClassPub(publicH1, classDict_publicH1, publicH1Out)
AddClassPub(publicH3, classDict_publicH3, publicH3Out)


#Go through private fastas and add clades from classification files to the 
#  end after a "|" delimiter
AddClassPriv(privateH1, classDict_privateH1, privateH1Out)
AddClassPriv(privateH3, classDict_privateH3, privateH3Out)









publicH1.close()
publicH3.close()
cladePubH1.close()
cladePubH3.close()
privateH1.close()
privateH3.close()
cladePrivH1.close()
cladePrivH3.close()
publicH1Out.close()
publicH3Out.close()
privateH1Out.close()
privateH3Out.close()












