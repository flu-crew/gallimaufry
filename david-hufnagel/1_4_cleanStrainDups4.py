#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to remove strain duplicates when the sequence is 
identical and store the others in a file to present to Zeb.
Created by David E. Hufnagel on Dec 22, 2020
This version handles the specific cases present in the OFFLU Fall 2021 data set
"""
import sys, random
inp = open(sys.argv[1]) #fasta input
outFasta = open(sys.argv[2], "w") #main fasta output
outDups = open(sys.argv[3], "w") #duplicates output



def SaveIntoDict(key, val, dictx):
    if key in dictx:
        dictx[key].append(val)
    else:
        dictx[key] = [val,]
        


#Go through the input and store all data in a dict of key: strain val: [(defline, seq), (defline, seq),...].
lastDefline = ""; lastStrain = ""; lastSeq = ""
inpDict = {}
for line in inp:
    if line.startswith(">"):
        defline = line.strip().strip(">")
        print(defline.split("|"))
        strain = defline.split("|")[-6]
        
        if lastDefline != "": #skip acting at the first defline
            SaveIntoDict(lastStrain, (lastDefline, lastSeq), inpDict)
        lastStrain = strain; lastDefline = defline; lastSeq = ""
    else:
        lastSeq += line.strip()
else:
    SaveIntoDict(lastStrain, (lastDefline, lastSeq), inpDict)
        

#Go through input dict and select a defline to keep where there are duplicates 
#  and the sequence is identical.  Make a list of deflines to keep.  Where 
#  sequences are not identical, output to outDups and keep both copies.
outputLst = []  #list of tuples of (defline, seq)
dupsLst = [] #list of tuples of (defline, seq)
for strain, data in inpDict.items():
    if len(data) == 1:
        outputLst.append((data[0][0], data[0][1]))
    else: #multiple instances of a strain name
        seqs = []
        deflines = []
        defsNoDate = [] #deflines with the dates removed
        for pair in data:
            deflines.append(pair[0])
            seqs.append(pair[1])
            defsNoDate.append("|".join(pair[0].split("|")[:-1]))
        if len(set(seqs)) == 1: #sequences are identical
            print("ERROR");sys.exit()  #in these case no sequences were identical
            # if len(seqs) == 2:
            #     if len(set(defsNoDate)) == 1: #deflines are identical other than date
            #         outputLst.append((random.choice(deflines), seqs[0])) #The dates are very close.  I therefore chose one randomly
            #     else:
            #         if strain in ["A/Swine/MB/NCFAD-048-10/2020", "A/Swine/MB/NCFAD-048-7"]:
            #              newDef = deflines[1].replace("|H1Nx|","|H1|")
            #              outputLst.append((newDef, seqs[0]))
            #         # else: #These were all cases of things being labeled as CVV or variant.  I went wint variant because the subtype always contains a "v" at the end
            #         #     outputLst.append((deflines[1], seqs[1]))
            # else:
            #     print("ERROR!")
            #     sys.exit()
        else: #sequences are different
            dupsLst.append((deflines[0], seqs[0]))
            dupsLst.append((deflines[1], seqs[1]))
            

#Go through outputLst and output everything
for pair in outputLst:
    newlines = ">%s\n%s\n" % (pair[0], pair[1])
    outFasta.write(newlines)


#Go through dupsLst and output everything
dupID = 1
for pair in dupsLst:
    newlines = ">%s__%s\n%s\n" % (pair[0], dupID, pair[1])
    dupID += 1
    outDups.write(newlines)












inp.close()
outFasta.close()
outDups.close()