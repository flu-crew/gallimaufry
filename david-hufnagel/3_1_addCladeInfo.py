#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to remove strain duplicates and put them in a separate
fasta file. This version is intended to be more general purpose than previous
versions. The only assumption is that the defline is "|" delimited. Where 
sequences and deflines are the same one is simply deleted and a message is 
sent to the screen. Where sequences are the same and deflines are not they
are one item in the dups.fna file with 2 deflines separated by "::"

Created by David E. Hufnagel on December 1, 2021
"""
import sys

inp = open(sys.argv[1])           #fasta input
outFasta = open(sys.argv[2], "w") #main fasta output
outDups = open(sys.argv[3], "w")  #duplicates output
loc = int(sys.argv[4]) - 1        #the index of the defline of the strain name (starting with 1)





def SaveIntoDict(key, val, dictx):
    if key in dictx:
        dictx[key].append(val)
    else:
        dictx[key] = [val,]

def ReadFasta(fd): #Go through input and store the file in a dict of key: strain   val: seq as well as a dict of key: strain  val: defline
    seqDict = {}; defDict = {}
    oldDef = ""; oldSeq = ""
    for line in fd:
        if line.startswith(">"):
            if oldSeq != "":
                oldStrain = oldDef.split("|")[loc]
                SaveIntoDict(oldStrain, oldSeq, seqDict)
                SaveIntoDict(oldStrain, oldDef, defDict)
                oldDef = line.strip().strip(">")
                oldSeq = ""
            else:
                oldDef = line.strip().strip(">")
        else:
            oldSeq += line.strip()
    else:
        oldStrain = oldDef.split("|")[loc]
        SaveIntoDict(oldStrain, oldSeq, seqDict)
        SaveIntoDict(oldStrain, oldDef, defDict)
    return(seqDict, defDict)





#Go through inp and generate a sequence dictionary and a defline dictionary
seqDict, defDict = ReadFasta(inp)


#Go through the sequence dictionary, output everything without duplicates and
#  put the rest in the duplicates file.  The only exception is where the
#  defline and seq are both identical.  In this case print this result
for strain, seq in seqDict.items():
    defline = defDict[strain]

    newlines = ">%s\n%s\n" % (defline[0], seq[0])
    if len(seq) == 1:                   #Simple no duplicate case
        outFasta.write(newlines)
    # elif len(seq) == 2:
    #     if seq[0] == seq[1]:            #Here the sequences are the same
    #         if defline[0] == defline[1]: #Here the deflines are the same as well
    #             outFasta.write(newlines)
    #             message = "%s was duplicated in defline and seq\n" % (strain)
    #             print(message)
    #         else:                       #Here the deflines are different, but the seqs are the same
    #             newlines = ">%s::%s\n%s\n" % (defline[0], defline[1], seq[0])
    #             outDups.write(newlines)
    #     else:                           #Here seqs are different
    #         newlines = ">%s\n%s\n" % (defline[0], seq[0])
    #         outDups.write(newlines)
            
    #         newlines = ">%s\n%s\n" % (defline[1], seq[1])
    #         outDups.write(newlines)
    elif len(seq) >= 2:
        if len(set(seq)) == 1: #Here the sequences are the same
            if len(set(seq)) == 1: #Here the deflines are the same as well
                outFasta.write(newlines)
                message = "%s was duplicated %s times in defline and seq\n" % (strain, len(seq))
                print(message)
            else:                       #Here the deflines are different, but the seqs are the same
                newlines = ">%s\n%s\n" % ("::".join(defline), seq[0])
                outDups.write(newlines)

        else:                           #Here seqs are different
            for i in range(len(seq)):
                newlines = ">%s_%s\n%s\n" % (defline[i], i+1, seq[i])
                outDups.write(newlines)
            






inp.close()
outFasta.close()
outDups.close()