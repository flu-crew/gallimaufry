"""
This script is designed to test the inputs for MEGAcc to see if we can identify 
the source of MEGAcc's error
Created by Dr. David E. Hufnagel Oct 30, 2020
"""
import sys

fasta = open(sys.argv[1])
final = open(sys.argv[2])
groups = open(sys.argv[3])



#Go through fasta and save deflines in a list
defLst = []
for line in fasta:
    if line.startswith(">"):
        defLst.append(line.strip().strip(">"))

    
#Go through groups file and save groups in a set


#Go through final file and look for ID's in the defline list
for line in final:
    defline = line.strip().split("=")[0]
    if not defline in defLst:
        print(defline)
        
    group = line.strip().split("=")[1]

    







fasta.close()
groups.close()
final.close()


