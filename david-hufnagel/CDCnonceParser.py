#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script processes a file called nonce.txt full of nonces and produces 
warning messages for repeated nonces.
Created by David E. Hufnagel on Mon Jul 31, 2023
"""
inp = open("nonce.txt")
out = open("nonce_warnings.txt", "w")
        
        
      
        
      
#Define dictionaries
def CalculateDiff(new, old):
    #extract new values
    newLst = new.split(":")
    newHour = float(newLst[0]); newMin = float(newLst[1]); newSec = float(newLst[2])
    
    #extract old values
    oldLst = old.split(":")
    oldHour = float(oldLst[0]); oldMin = float(oldLst[1]); oldSec = float(oldLst[2])
    
    #calculate new - old in minutes
    diff = (newHour*60 + newMin + newSec/60) - (oldHour*60 + oldMin + oldSec/60)
    
    return(diff)
        
        
      
           

#Go through inp and make a dictionary of key: nonce val: time of last nonce, 
#  with each new entry calculate the time difference between the current entry 
#  and the last one. If the difference is <= 5min, write a warning to out
lastNonces = {}
for line in inp:
    lineLst = line.strip().split()
    nonce = lineLst[0]
    date = lineLst[2] #I found that all the dates were the same so I did not use that variable in the diff calculations
    time = lineLst[-1] 
    
    if nonce in lastNonces:
        timeDiff = CalculateDiff(time, lastNonces[nonce])
        if timeDiff <= 5.0:
            warning = "Duplicate nonce: %s: current time %s %s last used %s %s\n" \
                % (nonce, date, time, date, lastNonces[nonce])
            out.write(warning)
        
        #update lastNonces using the fact that the current data is always newer than what is in lastNonces
        lastNonces[nonce] = time
    else:
        lastNonces[nonce] = time
    




inp.close()
out.close()




