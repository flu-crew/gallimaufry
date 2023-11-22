#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take names files containing IQ-TREE simplified 
deflines and summarize the region-related information present in them.
Created by David E. Hufnagel on Mon Mar  1 10:07:12 2021
"""
import sys


namesFd = open(sys.argv[1])
out = open(sys.argv[2], "w")




def SaveIntoCntDict(key, dictx):
    if key in dictx:
        dictx[key] += 1
    else:
        dictx[key] = 1
        
        


regionCnts = {}
for line in namesFd:
    lineLst = line.strip().split("_")

    #collect region data
    region = lineLst[3]
    if region in ["North", "South", "United", "Villa", "Pinar", "La", "Costa"]:
        region += "_"
        region += lineLst[4]
    elif region in ["4", ""]:
        region = lineLst[4]

    #set final region
    if region in ["Alberta", "Canada", "MB", "Manitoba", "QC", "Quebec", "SK", "Saskatchewan", "ON", "Ontario"]:
        region = "CAN"
    elif region in ["Costa_Rica", "Guatemala", "Holguin", "La_Habana", "Pinar_del", "Villa_Clara"]:
        region = "CentAmer"
    elif region in ["Guanajuato", "Jalisco", "MEX", "Mexico"]:
        region = "MEX"
    elif region in ["IL", "Ilinois", "Illinois"]:
        region = "IL"
    elif region in ["IN", "Indiana"]:
        region = "IN"
    elif region in ["MI", "Michigan"]:
        region = "MI"
    elif region in ["MN", "Minneosta", "Minnesota", "Minnestoa", "Minnoosta"]:
        region = "MN"
    elif region in ["MO", "Missouri"]:
        region = "MO"
    elif region in ["NC", "North_Carolina", "North_Carollina"]:
        region = "NC"
    elif region in ["OH", "Ohio"]:
        region = "OH"
    elif region in ["SD", "SouthDakota", "South_Dakota"]:
        region = "SD"
    elif region in ["IA", "Iowa"]:
        region = "IA"
    elif region in ["Memphis", "TN", "Tennessee"]:
        region = "TN"
    elif region in ["NE", "Nebraska"]:
        region = "NE"
    elif region == "Jamesburg":
        region = "NJ"
    elif region in ["USA", "United_States"]:
        region = "USA"
        
    SaveIntoCntDict(region, regionCnts)



for region, cnt in regionCnts.items():
    newline = "%s: %s\n" % (region, cnt)
    out.write(newline)




#add zeroz into the dict where necessary
if "CAN" not in regionCnts:
    regionCnts["CAN"] = 0
if "North_Dakota" not in regionCnts:
    regionCnts["North_Dakota"] = 0
if "MN" not in regionCnts:
    regionCnts["MN"] = 0
if "MI" not in regionCnts:
    regionCnts["MI"] = 0
if "OH" not in regionCnts:
    regionCnts["OH"] = 0
if "Pennsylvania" not in regionCnts:
    regionCnts["Pennsylvania"] = 0
if "Virginia" not in regionCnts:
    regionCnts["Virginia"] = 0
if "TN" not in regionCnts:
    regionCnts["TN"] = 0
if "Georgia" not in regionCnts:
    regionCnts["Georgia"] = 0
if "South_Carolina" not in regionCnts:
    regionCnts["South_Carolina"] = 0
if "NC" not in regionCnts:
    regionCnts["NC"] = 0
if "IA" not in regionCnts:
    regionCnts["IA"] = 0
if "Wisconsin" not in regionCnts:
    regionCnts["Wisconsin"] = 0
if "IL" not in regionCnts:
    regionCnts["IL"] = 0
if "MO" not in regionCnts:
    regionCnts["MO"] = 0
if "NE" not in regionCnts:
    regionCnts["NE"] = 0
if "SD" not in regionCnts:
    regionCnts["SD"] = 0
if "Kansas" not in regionCnts:
    regionCnts["Kansas"] = 0
if "Colorado" not in regionCnts:
    regionCnts["Colorado"] = 0
if "California" not in regionCnts:
    regionCnts["California"] = 0
if "Arizona" not in regionCnts:
    regionCnts["Arizona"] = 0
if "Texas" not in regionCnts:
    regionCnts["Texas"] = 0


#calculate region + neigboring regions and output
canPlus = regionCnts["CAN"] + regionCnts["North_Dakota"] + regionCnts["MN"] + \
    regionCnts["MI"] + regionCnts["OH"] + regionCnts["Pennsylvania"]
newline = "CANplus: %s\n" % (canPlus)
out.write(newline)

ncPlus = regionCnts["Virginia"] + regionCnts["TN"] + regionCnts["Georgia"] + \
    regionCnts["South_Carolina"] + regionCnts["NC"]
newline = "NCplus: %s\n" % (ncPlus)
out.write(newline)

iaPlus = regionCnts["IA"] + regionCnts["MN"] + regionCnts["Wisconsin"] + \
    regionCnts["IL"] + regionCnts["MO"] + regionCnts["NE"] + regionCnts["SD"]
newline = "IAplus: %s\n" % (iaPlus)
out.write(newline)

nePlus = regionCnts["SD"] + regionCnts["IA"] + regionCnts["MO"] + \
    regionCnts["Kansas"] + regionCnts["Colorado"] + regionCnts["NE"]
newline = "NEplus: %s\n" % (nePlus)
out.write(newline)

mexPlus = regionCnts["California"] + regionCnts["Arizona"] + regionCnts["Texas"]
newline = "MEXplus: %s\n" % (mexPlus)
out.write(newline)


namesFd.close()
out.close()
