#This script is designed to take an input fasta file and create a new file with
#only sequences that pass the given threshold for percent ambiguous bases
#Created by David E. Hufnagel on March 25, 2020

import sys
inp = open(sys.argv[1])      #input fasta file
thresh = float(sys.argv[2])  #percent ambigouous bases threshold
out = open(sys.argv[3], "w") #output fasta file



#Calculates percent ambiguous nucleotides from a string sequence
def CalcPerN(seq):
	numN = seq.count("N")+seq.count("n")
	tot = len(seq)
	return(float(numN) / float(tot)*100)



lastName = ""
currSeq = ""
firstName = True
for line in inp:
	if line.startswith(">"):
		if firstName == False:
			perN = CalcPerN(currSeq)
			if perN < thresh:
				newline = ">%s\n" % (lastName)
				out.write(newline)
				newline = "%s\n" % (currSeq)
				out.write(newline)
			currSeq = ""
			

		lastName = line.strip().strip(">")
		firstName = False
	else:
		currSeq += line.strip()
#Process the last sequence
else:
	perN = CalcPerN(currSeq)
	if perN < thresh:
		newline = ">%s\n" % (lastName)
		out.write(newline)
		newline = "%s\n" % (currSeq)
		out.write(newline)


inp.close()
out.close()
