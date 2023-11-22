#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script takes a fasta file with many sequences and a specific format, 
extracts dates, and outputs the range in this format:
Month Day, Year-Month Day, Year
Created by David on Sun Aug  2 14:40:09 2020
"""
import sys
inp = open(sys.argv[1])



def Reformat(first, last):
    fMonth = ConvertMonth(first[1])
    lMonth = ConvertMonth(last[1])
    newFirst = "%s %s, %s" % (fMonth, first[2], first[0])
    newLast = "%s %s, %s" % (lMonth, last[2], last[0])
    return(newFirst, newLast)

        
def ConvertMonth(num):
    if num == 1:
        return("Jan")
    elif num == 2:
        return("Feb")
    elif num == 3:
        return("Mar")
    elif num == 4:
        return("Apr")
    elif num == 5:
        return("May")
    elif num == 6:
        return("Jun")
    elif num == 7:
        return("Jul")
    elif num == 8:
        return("Aug")
    elif num == 9:
        return("Sep")
    elif num == 10:
        return("Oct")
    elif num == 11:
        return("Nov")
    elif num == 12:
        return("Dec")
    else:
        print("ERROR!")
        sys.exit()    
    



first = (2100,12,30)
last = (1900,1,1)
for line in inp:
    if line.startswith(">"):
        lineLst = line.strip().split("|")
        date = lineLst[-1]
        year = int(date.split("-")[0])
        month = int(date.split("-")[1])
        day = int(date.split("-")[2])
        
        #reset first if needed
        if year < first[0]:
            first = (year, month, day)
        elif year == first[0]:
            if month < first[1]:
                first = (year, month, day)
            elif month == first[1]:
                if day < first[2]:
                    first = (year, month, day)

        #reset last if needed
        if year > last[0]:
            last = (year, month, day)
        elif year == last[0]:
            if month > last[1]:
                last = (year, month, day)
            elif month == last[1]:
                if day > last[2]:
                    last = (year, month, day)
                    
#Print results
first, last = Reformat(first, last)
toPrint = "%s-%s\n" % (first, last)
print(toPrint)




inp.close()