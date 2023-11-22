"""This script is designed to take octoFLU results that identify certain
sequences as N2 that should be N1 and removing them from the aligned fasta
file with all sequences
Created by David E. Hufnagel on April 1, 2020
WARNING: THIS SCRIPT IS SITUATION SPECIFIC
"""
import sys

allSeqs = open(sys.argv[1])
n2Seqs = open(sys.argv[2])
out = open(sys.argv[3], "w") #allSeqs - n2Seqs



#Go through n2Seqs and make a list of the ID part of the strain name
n2ids = []
for line in n2Seqs:
	if line.startswith(">"):
		#ignore reference sequences
		if not (line.startswith(">LAIV") or line.startswith(">pdm") or \
			line.startswith(">classicalSwine") or \
			line.startswith(">humanSeasonal")):
			id = line.strip().split("A/swine/")[1].split("/")[1]
			n2ids.append(id)


#Go through allSeqs and output only sequences that are not in n2Seqs
#  while testing to make sure there are not multiple matches
usedIDs = []
lastSeq = ""
lastName = ""
firstName = True
for line in allSeqs:
	if line.startswith(">"):
		id = line.strip().split("/")[3]
		if not id in n2ids and not firstName:
			#write name and seq to output
			newline = ">%s\n" % (lastName)
			out.write(newline)
			newline = "%s\n" % (lastSeq)						
			out.write(newline)

			usedIDs.append(id)
		lastSeq = ""
		lastName = line.strip().strip(">")
		firstName = False
	else:
		lastSeq += line.strip()
#cleanup last sequence line
else:
	#write name and seq to output
	newline = ">%s\n" % (lastName)
	out.write(newline)
	newline = "%s\n" % (lastSeq)
	out.write(newline)



allSeqs.close()
n2Seqs.close()
out.close()
