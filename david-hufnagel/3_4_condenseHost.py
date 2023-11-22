#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script condenses host descriptions into only "Human", "Swine", "Avian", 
"Equine", "Other_mammal", and unknown
Created by David E. Hufnagel on Dec  3, 2022
"""
import sys

inp = open(sys.argv[1])
out = open(sys.argv[2], "w")





def CondenseHost(oldHost):
    if host in ["Barnacle_Goose","Avian","Bird","Blue_Winged_Teal","Chicken","Duck","Eurasian_Teal","Eurasian_Wigeon",\
                "Fowl","Goose","Gray_Teal","Green_Winged_Teal","Grey_Teal","Gull","Laughing_Gull","Mallard","Murre",\
                    "Northern_Pintail","Northern_Shoveler","Pintail","Quail","Ruddy_Turnstone","Rufous_Necked_Stint",\
                        "Sanderling","Shorebird","Teal","Thrush","Turkey","Waterfowl","Whooper_Swan","Wood_Duck",\
                            "Yellow_Billed_Teal"]:
        return("Avian")
    elif host in ["Human",]:
        return("Human")
    elif host in ["Swine", "Pig"]:
        return("Swine")
    elif host in ["Equine","Horse"]:
        return("Equine")
    elif host in ["Bat","Dog","little_yellow_shouldered_bat"]:
        return("Other_mammal")
    else:
        if host not in ["Environment", "Unknown"]:
            print("ERROR: no known category for %s" % (host))
            print("consider modifying condenseHost.py\n")
        return("unknown")





#Go through inp, extract host data and replace it using the CondenseHost 
#  function, output the result
for line in inp:
    if line.startswith(">"):
        lineLst = line.strip().split("|")
        host = lineLst[4]
        newHost = CondenseHost(host)
        lineLst[4] = newHost
        newData = "|".join(lineLst)
        newline = "%s\n" % (newData)
        out.write(newline)
        
    else:
        out.write(line)








inp.close()
out.close()