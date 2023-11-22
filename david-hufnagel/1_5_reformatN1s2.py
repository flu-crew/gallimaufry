#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take a fasta file of N1 sequences, completely
reformats the deflines so that they fit our standards,  and removes empty lines.
standard format: source|strain|subtype|host|country|clade|date (MM/DD/YYY)
*note the date format is not part of an established standard
Created by David E. Hufnagel on Fri Oct  5, 2020
"""
import sys

inp = open(sys.argv[1])
out = open(sys.argv[2], "w")



for line in inp:
    if line.startswith(">"):
        lineLst = line.strip().split("_")
        strain = "/".join(lineLst[:5]).strip(">"); subtype = lineLst[5]
        host = lineLst[1]; country = "CAN"; clade = ""; oldDate = lineLst[-1]
        newDate = "%s/%s/%s" % (oldDate.split("-")[1], oldDate.split("-")[2], oldDate.split("-")[0])
        newline = ">publicIAV|%s|%s|%s|%s|%s|%s\n" % (strain, subtype, host, country, clade, newDate)
        out.write(newline)
    else:
        if line.strip() not in ["","\n","^M"]:
            out.write(line)



inp.close()
out.close()
