#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take information in an OFFLU fasta defline and
use it to create a matadata table that could be read in MS Excel
Created by David E. Hufnagel on Tue Sep  7 10:29:12 2021
"""
import sys

inp = open(sys.argv[1])
out = open(sys.argv[2], "w")



title = "strain\tsubtype\thost\tclade\tcntry\tdate(YYYY-MM-DD)\tprovenance\tHItestInfo\n"
out.write(title)

for line in inp:
    if line.startswith(">") and "onsensus" not in line:
        lineLst = line.strip().split("|")
        strain = lineLst[-6]
        prov = lineLst[0].strip(">")
        subtype = lineLst[-5]
        host = lineLst[-4]
        cntry = lineLst[-3]
        clade = lineLst[-2]
        date = lineLst[-1]
        testInfo = ",".join(lineLst[1:-7]).strip(",")

        newLst = [strain, subtype, host, clade, cntry, date, prov, testInfo]
        for i in range(len(newLst)):
            if newLst[i] == "":
                newLst[i] = "NA"

        newline = "\t".join(newLst) + "\n"
        out.write(newline)






inp.close()
out.close()
