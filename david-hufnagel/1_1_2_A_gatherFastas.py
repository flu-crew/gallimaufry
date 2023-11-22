"""
This script is designed to take a file containing the names of sequences within
a fasta file and generating a smaller fasta file containing only those
sequences which have been named.
Created by David E. Hufnagel on Apr 22, 2020
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


#Go through fastaInp and output names in the list
lastName = ""
lastSeq = ""
firstName = True
for line in fastaInp:
    if line.startswith(">"):
        name = line.strip().strip(">")#.replace("|","_").replace("/","_")
        
        if firstName == False:
            if lastName in names:
                newline = ">%s\n" % (lastName)
                out.write(newline)
                newline = "%s\n" % (lastSeq.replace("-","")) #remove alignment dashes
                out.write(newline)
            lastSeq = ""

        lastName = name
        firstName = False
    else:
        lastSeq += line.strip()
#Process the last sequence
else:
	if lastName in names:
		newline = ">%s\n" % (lastName)
		out.write(newline)
		newline = "%s\n" % (lastSeq.replace("-","")) #remove alignment dashes
		out.write(newline)
	


fastaInp.close()
namesFd.close()
out.close()
