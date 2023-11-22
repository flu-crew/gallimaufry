"""
This script is designed to take a file containing the names of sequences within
a fasta file and generating a smaller fasta file containing only those
sequences which have been named in the order in which they were named.
Created by David E. Hufnagel on Oct 18, 2022
"""

import sys

fastaInp = open(sys.argv[1])
namesFd = open(sys.argv[2])
out = open(sys.argv[3], "w")





#Go through names file and store the names in a list
names = []
for line in namesFd:
    name = line.strip()
    names.append(name)


#Go through fastaInp and store the names in the list in a dict of key: name val: newlines
lastName = ""
lastSeq = ""
firstName = True
outDict = {}
for line in fastaInp:
    if line.startswith(">"):
        name = line.strip().strip(">")#.replace("|","_").replace("/","_")
        
        if firstName == False:
            if lastName in names:
                newlines = ">%s\n%s\n" % (lastName, lastSeq)
                outDict[lastName] = newlines                
                
            lastSeq = ""

        lastName = name
        firstName = False
    else:
        lastSeq += line.strip()
#Process the last sequence
else:
	if lastName in names:
            newlines = ">%s\n%s\n" % (lastName, lastSeq)
            outDict[lastName] = newlines
	

#Go through the name list and the output dict and output lines in order
for name in names:
    newlines = outDict[name]
    out.write(newlines)








fastaInp.close()
namesFd.close()
out.close()
