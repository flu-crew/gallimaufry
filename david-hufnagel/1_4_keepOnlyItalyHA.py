"""
This script is designed to take raw genomic sequences from Italian IAV and
keep only HA sequences.

Created by David E. Hufnagel on July 13, 2020
"""
import sys

inp = open(sys.argv[1])
out = open(sys.argv[2], "w")


toKeep = False
for line in inp:
    if line.startswith(">"):
        if line.strip().split("_")[-1] == "HA":
            toKeep = True
            out.write(line)
        else:
            toKeep = False
    else:
        if line != "\n" and toKeep == True:
            out.write(line)
                
            
        



inp.close()
out.close()

