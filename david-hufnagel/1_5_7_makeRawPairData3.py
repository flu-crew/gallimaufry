#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take a main fasta of NA sequences and an associated
fasta of HA sequences and make a resulting pair file with the format:
strain name    NA clade    HA clade    date

Created by David E. Hufnagel  Nov 10, 2020
Updated on Nov 17, 2020 for 10 years data
Updated on Jan 6, 2021 to add region information 
"""
import sys

fasta = open(sys.argv[1])         #n1s10yrs_v4_lowerSwine_simp.fna
naCladesFd = open(sys.argv[2])    #namesWgroups.txt
cladeColorsFd = open(sys.argv[3]) #cladeColors2.txt
out1 = open(sys.argv[4], "w")     #pairData_10yr_1.txt
out2 = open(sys.argv[5], "w")     #pairData_10yr_2.txt
out3 = open(sys.argv[6], "w")     #pairData_10yr_3.txt
out4 = open(sys.argv[7], "w")     #pairData_10yr_4.txt
out5 = open(sys.argv[8], "w")     #pairData_10yr_5.txt
outC = open(sys.argv[9], "w")     #pairData_10yr_CAN.txt
outM = open(sys.argv[10], "w")    #pairData_10yr_MEX.txt



def ReformatDate(oldDate):
        slashes = oldDate.count("-")
        
        if slashes == 2:   
            oldDateLst = oldDate.split("-")
            year = oldDateLst[2]; month = oldDateLst[0]; day = oldDateLst[1]
            newDate = "%s-%s-%s" % (year, month, day)
        elif slashes == 1:
            oldDateLst = oldDate.split("-")
            year = oldDateLst[1]; month = oldDateLst[0]
            newDate = "%s-%s" % (year, month)
        else:
            newDate = oldDate
            
        return(newDate)
    

def CleanupStates(stateData):
    if stateData[0] in ["Costa", "La", "North", "South", "Villa"]:
        state = "_".join(stateData[:2])
    elif stateData[0] == "Pinar":
        state = "_".join(stateData[:3])
    elif stateData[0] in ["IL", "Ilinois"]:
        state = "Illinois"
    elif stateData[0] == "IN":
        state = "Indiana"
    elif stateData[0] == "MI":
        state = "Michigan"
    elif stateData[0] == "MN":
        state = "Minnesota"
    elif stateData[0] == "MO":
        state = "Missouri"
    elif stateData[0] == "NC":
        state = "North_Carolina"
    elif stateData[0] == "OH":
        state = "Ohio"
    elif stateData[0] == "OR":
        state = "Oregon"
    elif stateData[0] == "SD":
        state = "South_Dakota"
    else:
        state = stateData[0]
        
        
    if state == "North_Carollina":
        state = "North_Carolina"
    elif state == "SouthDakota":
        state = "South_Dakota"
    elif state in ["Minnestoa", "Minneosta", "Minnoosta"]:
        state = "Minnesota"
    elif state in ["United", "USA"]:
        state = "NA"    
        
    
    return(state)


def StateToRegion(state):
    if state in ["Washington", "Oregon", "California", "Nevada", "Alaska", \
                 "Hawaii", "Utah", "New Mexico", "Arizona", "Colorado"]:
        reg = 5
    elif state in ["Idaho", "Montana", "Wyoming", "North_Dakota", \
                   "South_Dakota", "Nebraska", "Kansas"]:
        reg = 4
    elif state in ["Texas", "Oklahoma", "Missouri", "Arkansas", \
                   "Luisiana", "Mississippi"]:
        reg = 3
    elif state in ["Minnesota", "Iowa", "Wisconsin", "Illinois", "Michigan", \
                   "Indiana", "Kentucky", "Ohio"]:
        reg = 2
    elif state in ["Tennessee", "Alabama", "Florida", "Georgia", \
                   "South_Carolina", "North_Carolina", "Virginia", \
                       "West_Virginia", "Maryland", "Delaware", \
                           "Pennsylvania", "New_Jersey", "New York", \
                               "Connecticut", "Rhode Island", "Massachusetts", \
                                   "Vermont", "New_Hampshire", "Maine", "Puerto_Rico"]:
        reg = 1
    elif state in ["British_Columbia", "Alberta", "Saskatchewan", \
                   "Manitoba", "Ontario", "Quebec", \
                       "Newfoundland_and_Labrador", "New_Brunswick", \
                           "Nova_Scotia", "Prince_Edward_Island"]:
        reg = "CAN"
    elif state in ["Jalisco", "Guanajuato", "Mexico"]:
        reg = "MEX"
    elif state in ["Costa_Rica", "Guatemala", "Holguin", "La_Habana", \
                   "Pinar_del_Rio", "NA", "Villa_Clara"]:
        reg = "Other"
    else:
        print(state)
        sys.exit()
    
    return(reg)





#Go through clade colors and make a dict of key: color  val: clade
cladeColorDict = {}
for line in cladeColorsFd:
    lineLst = line.strip().split("\t")
    color = lineLst[0]; clade = lineLst[1]
    cladeColorDict[color] = clade
    
    
#Go through na clades and make a dict of key: strain  val: naClade
cladeDict = {}
for line in naCladesFd:
    color = line.strip().split("=")[1]
    #change newBlack to black
    if color == "newBlack":
        color = "black"
    
    clade = cladeColorDict[color]
    strain = "A_swine_" + "_".join(line.strip().split("swine")[1].strip("_").split("Swine")[0].strip("_").split("_")[:-1])

    cladeDict[strain] = clade


#Output titles
title = "#strain\tNAclade\tHAclade\tregion\tdate\n"
out1.write(title);out2.write(title);out3.write(title);out4.write(title)
out5.write(title);outC.write(title);outM.write(title)


#Go through fasta, collect all data, and generate the output 
for line in fasta:
    if line.startswith(">"):
        strain = "A_swine_" + "_".join(line.strip().split("swine")[1].strip("_").split("Swine")[0].strip("_").split("_")[:-1])
        haClade = line.split("Swine")[1].split("_")[2]
        
        #correct for problems created by IQTREE's replacement of special characters with underscores
        if not (haClade.startswith("1A") or haClade.startswith("1B") or haClade.startswith("1C")):
            haClade = line.split("Swine")[1].split("_")[3]
        date = "-".join(line.split("Swine")[1].strip("_").split("_")[2:]).strip()
        if "1A" in date:
            date = "-".join(date.split("-")[1:])
        
        if "like" in date:
            extra = "-" + date.split("-like-")[0] + "-like"
            date = date.split("like-")[1]
            haClade += extra
            
        if haClade.count("-") > 2:
            haClade = haClade.split("-09-14")[0]
        
            
        naClade = cladeDict[strain]        
        newDate = ReformatDate(date)
        
        #determine the region
        state = CleanupStates(strain.split("_")[2:-2])
        region = StateToRegion(state)
        
        newline = "%s\t%s\t%s\t%s\t%s\n" % (strain, naClade, haClade, region, newDate)
        if region == 1:
            out1.write(newline)
        if region == 2:
            out2.write(newline)
        if region == 3:
            out3.write(newline)
        if region == 4:
            out4.write(newline)
        if region == 5:
            out5.write(newline)
        if region == "CAN":
            outC.write(newline)
        if region == "MEX":
            outM.write(newline)
            





fasta.close()
naCladesFd.close()
cladeColorsFd.close()
out1.close()
out2.close()
out3.close()
out4.close()
out5.close()
outC.close()
outM.close()