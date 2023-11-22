#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script changes all unknown clade information to N1.E
Created on Thu Sep 28 11:33:57 2023 by David E. Hufnagel
"""
inp = open("combined_clean_class.aln")
out = open("combined_clean_class_plusN1E.aln", "w")




for line in inp:
    if line.startswith(">"):
        lineLst = line.strip().strip(">").split("|")
        clade = lineLst[-3]
        if clade == "":
            lineLst[-3] = "N1.E"
        newline = ">" + "|".join(lineLst) + "\n"
        out.write(newline)
    else:
        out.write(line)

inp.close()
out.close()