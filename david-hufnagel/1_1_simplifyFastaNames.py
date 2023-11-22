"""
This script is designed to take an input fasta file with the special 
characters "|" and "/" and replace them all with "_"
Created by David E. Hufnagel on May 7, 2020
"""
import sys


inp = open(sys.argv[1])
out = open(sys.argv[2], "w")



for line in inp:
    if line.startswith(">"):
        out.write(line.replace("|","_").replace("/","_").replace("=", "_")\
                  .replace("[", "_").replace("]", "_").replace(" ", "_").replace("'","_"))#\.replace("-", "_"))
    else:
        out.write(line)




inp.close()
out.close()


