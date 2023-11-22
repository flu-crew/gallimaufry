"""
This script is designed to take a file which lists of names representing 
samples from a tree and another file which lists names to remove from the first
file and produces the original file minus removed samples.
Created by David E. Hufnagel on May 7, 2020
Updated on June 22, 2021 to use two input files with slightly different formats
"""

import sys

allNamesFd = open(sys.argv[1])
subtractNamesFd = open(sys.argv[2])
out = open(sys.argv[3], "w")



#Make a list of names in subtractNamesFd
subtractNames = []
for line in subtractNamesFd:
    if "onsensus" not in line:
        lineLst = line.strip().split("|")
        clade = "_".join(lineLst[5].split("_")[:-1])
        lineLst[5] = clade
        newline = "%s\n" % ("|".join(lineLst))
        subtractNames.append(newline.strip())

#Go through allNamesFd and and output all names not in subtractNamesFd
for line in allNamesFd:
    name = line.strip()
    if name not in subtractNames:
        nameLst = name.split("|")
        clade = nameLst[5] + "_C3"
        nameLst[5] = clade
        newline = "%s\n" % ("|".join(nameLst))
        out.write(newline)




allNamesFd.close()
subtractNamesFd.close()
out.close()