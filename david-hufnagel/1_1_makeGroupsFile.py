"""
This script combines one name per line names files into a groups file for 
MEGAcc.
Created by David E. Hufnagel on May 7, 2020
"""

import sys
namesFiles = open(sys.argv[1])   #a file containing the names of names files, one line per filename
fileOfNames = open(sys.argv[2])  #the names of groups in one file with one name per line
out = open(sys.argv[3], "w")     #The new groups file which can be used in MEGAcc


#Go through fileOfNames and make a list of group names in order
groupNames = []
for line in fileOfNames:
    groupNames.append(line.strip())

#Go through namesFiles, open each file within the fofn, iterate through
#  sequence names and modify them such that they have the group name on the
#  end, finally output these names
cnt = 0
for namesFile in namesFiles:
    namesFileFd = open(namesFile.strip())
    
    
    for line in namesFileFd:
        name = line.strip()
        newLine = "%s=%s\n" % (name, groupNames[cnt])
        out.write(newLine)
        
    cnt += 1
    namesFileFd.close()
        




namesFiles.close()
fileOfNames.close()
out.close()