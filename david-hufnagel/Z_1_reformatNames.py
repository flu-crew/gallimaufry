# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import sys

inp = open(sys.argv[1])
out = open(sys.argv[2], "w")



for line in inp:
    if line.startswith(">"):
        if line.startswith(">A/Hunan"):
            out.write(line)
        elif line.startswith(">lcl|"):
            segment = line.split(" ")[1].strip("[]")[5:]
            acc = line.split(" ")[0].split("_")[0][5:-2]
            if acc in ["KY250316","KY250317","KY250318","KY250319","KY250320","KY250321","KY250322","KY250323"]:
                strain = "A/Netherlands/3315/2016"
            elif acc in ["KY368147","KY368148","KY368149","KY368150","KY368152","KY368153","KY368151","KY368154"]:
                strain = "A/Pavia/65/2016"
            newline = ">%s|%s\n" % (strain, segment)
            out.write(newline)
        else:
            strain = line.split(" ")[1]
            segment = line.split("(")[1].strip()[:-1]
            newline = ">%s|%s\n" % (strain, segment)
            out.write(newline)
    else:
        out.write(line)
        
        
        
        
inp.close()
out.close()