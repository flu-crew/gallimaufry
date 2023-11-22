"""
This script is designed to compare names files across data sets and selected 
sequences from the 2 years data set to determine how representative strains
and clades selected using 2-years data are when all data is considered.
Created by Dr. David E. Hufnagel on Tue Jul  7, 2020
"""

import sys, os

namesFiles_2 = sys.argv[1] #a folder of names files for 2 year data
namesFiles_5 = sys.argv[2] #a folder of names files for 5 year data
namesFiles_A = sys.argv[3] #a folder of names files for all years data
repSeqs = open(sys.argv[4])      #a file of representative sequences from 2 years data clades
out = open(sys.argv[5], "w")     #a report summarizing results



def SaveIntoDict(key, val, dictX):
    if key not in dictX:
        dictX[key] = [val]
    else:
        dictX[key].append(val)
        
        
def ProcessNames(folder):
    myDict = {}
    reverseDict = {}
   
    for filex in os.listdir(folder):
        group = filex.split("ames.txt")[0][:-1].strip("_")
        
        fullFileName = "%s%s" % (folder, filex)
        fd = open(fullFileName)
        for line in fd:
             #Make a dict of key: groupName   val: names list.
            SaveIntoDict(group, line.strip(), myDict)
            
            #Make a dict of key: seqName   val: cladeName
            reverseDict[line.strip()] = group
                
        fd.close()

    return(myDict, reverseDict)

    
    
            
            


#Iterate through names files, and store names data in dicts of key: groupName,
#  val: names list.  Also makes a dict of key: seqName   val: cladeName
namesDict_2, revDict2 = ProcessNames(namesFiles_2)
namesDict_5, revDict5 = ProcessNames(namesFiles_5)
namesDict_A, revDictA = ProcessNames(namesFiles_A)


#Iterate through repSeqs and store data in a list.
refSeqLst = []
for line in repSeqs:
    refSeqLst.append(line.strip())
    
    
#For each 2yr clade determine what percent of sequences in the clade are
#  present in the 5 year and all year clade where the reference sequence
#  resides.  Also makes a dict of key: cladeName  val: refSeq
refClades = {} # dict of key: cladeName  val: refSeq
cladePercents5 = {} # a dict of key: cladeName  val: percent ref membership in 5 years data
cladePercentsA = {} # a dict of key: cladeName  val: percent ref membership in 5 years data
missingPer5 = {} # a dict of key: cladeName val: percent missing ref in 5 years data
missingPerA = {} # a dict of key: cladeName val: percent missing ref in all years data

for clade in namesDict_2.keys():
    #Go through all sequences in a 2 year clade, and when a refseq is found 
    #  capture its 5yr and allyr clade
    namesLst = namesDict_2[clade]
    refClade5 = ""; refCladeA = ""
    for name in namesLst:
        if name in refSeqLst:
            refClade5 = revDict5[name] #the clade where the ref seq resides in 5 year tree
            refCladeA = revDictA[name] #the clade where the ref seq resides in all years tree
            refClades[clade] = name
            break
    
    #Go through all sequences in a 2 year clade again, and add to a counter
    #  based on whether the clade in 5 or all years data is the same as the
    #  one from the refseq
    inClade5 = 0; outClade5 = 0; inCladeA = 0; outCladeA = 0
    missing5 = 0; missingA = 0 #to keep track of where a 2 year name is not in a larger data set
    for name in namesLst:
        if name in revDict5:
            nameClade5 = revDict5[name] #the clade where this seq resides in 5 year tree
        else:
            missing5 += 1
            continue
        
        if name in revDictA:
            nameCladeA = revDictA[name] #the clade where this seq resides in all years tree
        else:
            missingA += 1
            continue
        
        if nameClade5 == refClade5:
            inClade5 += 1
        else:
            outClade5 += 1
            
        if nameCladeA == refCladeA:
            inCladeA += 1
        else:
            outCladeA += 1
    
    #Use counters to calculate and save a percentage of clade membership overlap
    perMemb5 = (float(inClade5) / (float(inClade5) + float(outClade5))) * 100.0
    perMembA = (float(inCladeA) / (float(inCladeA) + float(outCladeA))) * 100.0
    
    cladePercents5[clade] = perMemb5
    cladePercentsA[clade] = perMembA
    missingPer5[clade] = missing5
    missingPerA[clade] = missingA
    

#Output results in a tabular format
#2yrCladeName   refSeq   5yrCladeFromRef   allyrCladeFromRef   percent2yrMembersIn5yrRefClade   percent2ryMembersInAllyrRefClade   missingPercent2yrMembersIn5yrRefClade   missingPercent2ryMembersInAllyrRefClade
out.write("2yrCladeName   refSeq   5yrCladeFromRef   allyrCladeFromRef   percent2yrMembersIn5yrRefClade   percent2ryMembersInAllyrRefClade   missingPercent2yrMembersIn5yrRefClade   missingPercent2ryMembersInAllyrRefClade\n")
for refName in refSeqLst:
    #Gather data
    clade2yr = revDict2[refName]
    clade5yr = revDict5[refName]
    cladeAyr = revDictA[refName]
    percent5yr = cladePercents5[clade2yr]
    percentAyr = cladePercentsA[clade2yr]
    missing5yr = missingPer5[clade2yr]
    missingAyr = missingPerA[clade2yr]
    
    #Output data
    newline = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (clade2yr, refName, clade5yr, cladeAyr, percent5yr, percentAyr, missing5yr, missingAyr)
    out.write(newline)
    




repSeqs.close()
out.close()
