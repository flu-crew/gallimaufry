#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take the HA1 trimmed amino acid sequence data from
   a set of data points which are outliers by way of having low amino acid 
   distance and high antigenic distance (the positive set) and a set of data 
   points which are outliers by way of having low amino acid distance and low 
   antigenic distance (the negative set) and looking for amino acids 
   substitutions that may be significant for antigenic shift.
Created by David E. Hufnagel on Mon May 24, 2021
"""
import sys

fasta = open("gammaProjMergedData_all_noACC_pdmGamma_MN45fix_trim.faa")
commonSeqs0616 = open("gammaSeqs06_16_v2_trim_311lenFilt.aln")
commonSeqs2021 = open("gammaSeqs20_21_clean_trim.aln")
posFD = open("gammaMerged_compareAAdiffHIdiff_1A.3.3.3_outliers.tab")
negFD = open("gammaMerged_compareAAdiffHIdiff_1A.3.3.3_negatives.txt")
out = open("gammaProjMergedDataSigAAs.txt", "w")





def SaveIntoCntDict(key, dictx):
    if key in dictx:
        dictx[key] += 1
    else:
        dictx[key] = 1
        

def ModifyName(oldName):
    if oldName == "A/SWINE/OHIO/511445/2007":
        return("A/SWINE/OH/511445/2007")
    if oldName == "A/OHIO/9/2015":
        return("A/OHIO/09/2015")
    else:
        return(oldName)
    
    
def FillHashTable(fd, myHash, myAALst):
    fd.readline()
    for line in fd:
        lineLst = line.strip().split("\t")
        strainA = ModifyName(lineLst[1].split(" ")[0])
        strainB = ModifyName(lineLst[3].split(" ")[0])
     
        seqA = seqDict[strainA]
        seqB = seqDict[strainB]
        
        for locus in range(len(seqA)):  #both seqs should be the same length
            aaA = seqA[locus]
            aaB = seqB[locus]
            
            if aaA != aaB and (aaA not in ["x","X"] and aaB not in ["x","X"]):
                myHash[locus] += 1
                myAALst[locus].append((aaA,aaB))    
        
                
def BuildSeqsByLoc(fd, seqsBL):
    i = 0
    for line in fd:
        if not line.startswith(">"):
            for aa in line.strip():
                seqsBL[i].append(aa)
                i += 1
        else:
            i = 0 
           
            
#This version is for the 2006-2016 data which has a few frameshifts in it we need to skip past for proper and equivalent numbering
def BuildSeqsByLoc2(fd, seqsBL):
    i = 0
    for line in fd:
        if not line.startswith(">"):
            for aa in line.strip():
                if i <=152:
                    seqsBL[i].append(aa)
                elif i > 154:# and i < 282: #skipping two
                    seqsBL[i-2].append(aa)
                # elif i > 282:  #skipping one
                #     seqsBL[i-3].append(aa)
                i += 1
        else:
            i = 0 
       
            
# def LoadAAprofiles(seqsByLoc, aaProfile):
#     i = 0
#     for locus in seqsByLoc:
#         aasPresent = list(set(locus))
#         if len(aasPresent) == 1:
#             aaProfile[i] = (locus[0], 100)
#         elif len(aasPresent) == 2:
#             cntA = locus.count(aasPresent[0])
#             cntB = locus.count(aasPresent[1])
            
#             if cntA > cntB:
#                 first = aasPresent[0]
#                 firstCnt = cntA
                
#                 sec = aasPresent[1]
#                 secCnt = cntB
#             elif cntA < cntB:
#                 first = aasPresent[1]
#                 firstCnt = cntB
                
#                 sec = aasPresent[0]
#                 secCnt = cntA
                
#             firstPerc = float(firstCnt) / float(len(locus))
#             secPerc = float(secCnt) / float(len(locus))    
#             aaProfile[i] = [(first, firstPerc), (sec, secPerc)]
#         elif len(aasPresent) > 2:
#             firstCnt = 0; secCnt = 0
#             isTiedSeconds = False; tiedSeconds = []
#             first = ""; sec = ""
#             for aa in aasPresent:
#                 aaCnt = locus.count(aa)
#                 if aaCnt > firstCnt:
#                     secCnt = firstCnt
#                     sec = first
#                     if firstCnt != secCnt:
#                         isTiedSeconds = False
#                         tiedSeconds = []
#                     else:
#                         isTiedSeconds = True
#                         tiedSeconds = [first, sec]
             
#                     first = aa
#                     firstCnt = aaCnt
    
#                 elif aaCnt > secCnt:
#                     sec = aa
#                     secCnt = aaCnt
#                     isTiedSeconds = False
#                     tiedSeconds = []
#                 elif aaCnt == secCnt:
#                     isTiedSeconds = True
#                     tiedSeconds.append(sec)
#                     tiedSeconds.append(aa)
                    
#             if isTiedSeconds:
#                 sec = list(set(tiedSeconds))
#             if len(sec) == 1:
#                 sec = sec[0]
                
#             firstPerc = float(firstCnt) / float(len(locus))
#             secPerc = float(secCnt) / float(len(locus)) 
#             aaProfile[i] = [(first, firstPerc), (sec, secPerc)]
        
#         i += 1
        
#     return(aaProfile)


def LoadCompleteAAprofiles(seqsByLoc, aaProfile):
    i = 0
    for locus in seqsByLoc:
        total = 0
        for aa in locus:
            SaveIntoCntDict(aa, aaProfile[i])
            total += 1
        
        #convert counts into percetages
        percentTemp = {}  #This is a temporary standin for aaProfile[i] becasue it's dangerous to change something while one iterates through it
        for aa, cnt in aaProfile[i].items():
            perc = float(cnt) / float(total)
            percentTemp[aa] = perc
        
        #percentTemp = list(percentTemp)
        #percentTemp.sort()
        aaProfile[i] = percentTemp
            
        i += 1
    return(aaProfile)

            

    

#Go through fasta and make a dict of key: strain  val: seq.  Also make two 
#   lists of zeroes the length of the sequences that function as hash tables
#   in order to record  the number of positive and negative hits at each locus 
#   also make two similar lists which contain lists instead of zeroes in order
#   to capture which specific amino acids tend to be involved.  Also make two
#   lists of lists that will be used to store seqs by locus
seqDict = {}
lenSeq = 0
lastStrain = ""; lastSeq = ""
for line in fasta:
    if line.startswith(">"):
        if lastSeq != "":
            seqDict[lastStrain] = lastSeq
            
        strain = line.strip(">").split("|")[0].upper()
        lastStrain = strain
        lenSeq = len(lastSeq)
        lastSeq = ""
    else:
        lastSeq += line.strip()
else:
    seqDict[lastStrain] = lastSeq

        
##Now for the hash tables
posHash = []; negHash = []  #remember that this starts at 0, and 1 will need to be added at the end
posAAs = []; negAAs = []
seqsByLoc0616 = []; seqsByLoc2021 = []
aaProfile0616 = []; aaProfile2021 = []
for i in range(lenSeq):
    posHash.append(0)
    negHash.append(0)
    
    posAAs.append([])
    negAAs.append([])
    
    seqsByLoc0616.append([])
    seqsByLoc2021.append([])
    aaProfile0616.append({})
    aaProfile2021.append({})
    

#Go through the fasta again and store seqsByLoc with all sequences seperated by locus
BuildSeqsByLoc2(commonSeqs0616, seqsByLoc0616)
BuildSeqsByLoc(commonSeqs2021, seqsByLoc2021)
        

#Go through seqsByLoc, determine the amino acid profile, and store it in a
#  list of dicts of key: aa  val: aaCnt
aaProfile0616 = LoadCompleteAAprofiles(seqsByLoc0616, aaProfile0616) 
aaProfile2021 = LoadCompleteAAprofiles(seqsByLoc2021, aaProfile2021) 

#Go through posFD and negFD, and for every pair gather sequence data and 
#   compare them identifying differences that do not include "X", because it 
#   mean's missing data, and add to the hash tables
FillHashTable(posFD, posHash, posAAs)
FillHashTable(negFD, negHash, negAAs)


#Go through both hash tables simultaneously and output the positive and 
#   negative values for each amino acid
title = "locus\tposCnt\tnegCnt\tposAAs\tnegAAs\taaProfile2006-2016\taaProfile2020-2021\n"
out.write(title)
for i in range(lenSeq):
    locus = i + 1
    posCnt = posHash[i]
    negCnt = negHash[i]
    
    posAAset = posAAs[i]
    negAAset = negAAs[i]
    
    #aaDist0616 = list(aaProfile0616[i].items())
    #aaDist2021 = list(aaProfile2021[i].items())
    aaDist0616 = list({k: v for k, v in sorted(aaProfile0616[i].items(), key=lambda item: item[1], reverse=True)}.items())
    aaDist2021 = list({k: v for k, v in sorted(aaProfile2021[i].items(), key=lambda item: item[1], reverse=True)}.items())
    
    
    newline = "%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (locus, posCnt, negCnt, posAAset, negAAset, aaDist0616, aaDist2021)
    out.write(newline)


######TO IMPROVE 1) split input fastas into gamma clades 2) count every amino acid, not just the top 2



fasta.close()
commonSeqs0616.close()
commonSeqs2021.close()
posFD.close()
negFD.close()
out.close()