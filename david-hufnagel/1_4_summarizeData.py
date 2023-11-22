#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to summarize data and answer specific questions 
for Amy Vincent
Created by David E. Hufnagel on July 15, 2020
"""
import sys

fasta = open(sys.argv[1])
cladeInfo = open(sys.argv[2])
overTimeOut = open(sys.argv[3], "w")
geographyOut = open(sys.argv[4], "w")



#Go through cladeInfo and make a dict of key: name  val: clade


#Go thorugh fasta and make the following lists of tuples, 1) for 1C.2.3 
#  (date, name) 2) for 1C (date, name)






fasta.close()
cladeInfo.close()
overTimeOut.close()
geographyOut.close()