#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 14:24:34 2023

@author: david.hufnagel
"""

inpN1c21 = open("N1.C.2.1_names.txt") 
inpN1c32 = open("N1.C.3.2_names.txt")
inpN1e = open("N1.E_names.txt")
inpN1p = open("N1.P_names.txt")
outDetailed = open("classReport_detailed.txt", "w")
outSumm = open("classReport_summary.txt", "w")





#FUNCTIONS
def Process(cnt, inp, name):
    for line in inp:
        if "REF" not in line:
            cnt += 1
            
            strain = line.strip().split("|")[0]
            newline = "%s\t%s\n" % (strain, name)
            outDetailed.write(newline)    

    return(cnt)


#BODY
n1c21Cnt = 0
n1c21Cnt = Process(n1c21Cnt, inpN1c21, "N1.C.2.1")

n1c32Cnt = 0
n1c32Cnt = Process(n1c32Cnt, inpN1c32, "N1.C.3.2")

n1eCnt = 0
n1eCnt = Process(n1eCnt, inpN1e, "N1.E")

n1pCnt = 0
n1pCnt = Process(n1pCnt, inpN1p, "N1.P")


newline = "N1.C.2.1\t%s\n" % (n1c21Cnt)
outSumm.write(newline)

newline = "N1.C.3.2\t%s\n" % (n1c32Cnt)
outSumm.write(newline)

newline = "N1.E\t%s\n" % (n1eCnt)
outSumm.write(newline)

newline = "N1.P\t%s\n" % (n1pCnt)
outSumm.write(newline)









inpN1c21.close()
inpN1c32.close()
inpN1e.close()
inpN1p.close()
outDetailed.close()
outSumm.close()