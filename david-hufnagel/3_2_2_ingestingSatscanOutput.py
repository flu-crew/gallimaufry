#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take SaTScan output as its input and convert the
data from all files into one tab delimited file which can be used by R for
plotting. In this case we're only using Poisson data for clades and ignoring
decreased RR.
Created by David E. Hufnagel on Mon Apr  4, 2022
"""
import sys, copy
inp_n1c1x = open("N1C1X.txt")
inp_n1c2 = open("N1C2.txt")
inp_n1c21 = open("N1C21.txt")
inp_n1c3 = open("N1C3.txt")
inp_n1c31 = open("N1C31.txt")
inp_n1c32 = open("N1C32.txt")
inp_n1p = open("N1P.txt")
out_all = open("satsPoissResults_clades_all.txt", "w")
out_Up = open("satsPoissResults_clades_up.txt", "w")
out_Up_RR2 = open("statsPoissResults_clades_up_rr2.txt", "w")
out_Up_RR2_cases10 = open("statsPoissResults_clades_up_rr2_cases10.txt", "w")
out_stateID = open("stateIDsPoiss.txt", "w")





#Define functions
def IngestInput(inp, clade, dictx):
    
    #Gather data into a dictionary of key: clusterNum val: [region, cases, rr, startTime, stopTime]
    clustersDict = {} #a dict containing key: clusterNum val: [region, cases, rr, startTime, stopTime]
    clusterNum = 0
    record = False #whether we have yet hit the data lines we are ingesting
    regionData = ""  #a stand-in for the collection of states that relate to one cluster
    readingRegion = False #whether we are taking in region information for one cluster
    for line in inp:
        #Identify relevant data lines
        if "Location IDs included" in line:
            record = True
        elif "_______" in line:
            record = False
            
        #collect data seperated by cluster
        if record:            
            if "Location IDs included" in line: #new cluster begins
                clusterNum += 1
                regionData += line.strip()
                readingRegion = True
                continue
            if readingRegion:
                if ":" in line: #end cluster and reset region data
                    region = GenerateRegion(regionData)
                    clustersDict[clusterNum] = [region,"cas","rr","start","stop"]
                    
                    readingRegion = False
                    regionData = ""
                else: #add to region
                    regionData += line.strip()
                   
        #collect number of cases
        if "Number of cases" in line:
            cas = line.split(":")[-1].strip()
            clustersDict[clusterNum][1] = cas
                   
        #collect RR
        if "Relative risk" in line:
            rr = line.split(":")[-1].strip()
            clustersDict[clusterNum][2] = rr

        #collect start time range
        if "Time frame" in line:
            start = line.split(":")[-1].split()[0].strip()
            clustersDict[clusterNum][3] = ReformatDate(start)
        
        #collect stop time range
        if "Time frame" in line:
            stop = line.split(":")[-1].split()[2].strip()
            clustersDict[clusterNum][4] = ReformatDate(stop)        
            
    dictx[clade] = clustersDict
    
    
#Converts full state names to state abbreviations and combines with a consistent format
def GenerateRegion(dataChunk):
    allStates = dataChunk.split(":")[-1].strip().split(",")
    allStates2 = []
    for state in allStates:
        state = state.strip().replace("West Virginia","WV").replace("Alabama","AL").replace("Alaska","AK").replace("Arizona","AZ")\
            .replace("Arkansas","AR").replace("California","CA").replace("Colorado","CO").replace("Connecticut","CT").replace("Delaware","DE")\
                .replace("Florida","FL").replace("Georgia","GA").replace("Hawaii","HI").replace("Idaho","ID").replace("Illinois","IL")\
                    .replace("Indiana","IN").replace("Iowa","IA").replace("Kansas","KS").replace("Kentucky","KY").replace("Louisiana","LA")\
                        .replace("Maine","ME").replace("Maryland","MD").replace("Massachusetts","MA").replace("Michigan","MI")\
                            .replace("Minnesota","MN").replace("Mississippi","MS").replace("Missouri","MO").replace("Montana","MT")\
                                .replace("Nebraska","NE").replace("Nevada","NV").replace("New Hampshire","NH").replace("New Jersey","NJ")\
                                    .replace("New Mexico","NM").replace("New York","NY").replace("North Carolina","NC")\
                                        .replace("North Dakota","ND").replace("Ohio","OH").replace("Oklahoma","OK").replace("Oregon","OR")\
                                            .replace("Pennsylvania","PA").replace("Rhode Island","RI").replace("South Carolina","SC")\
                                                .replace("South Dakota","SD").replace("Tennessee","TN").replace("Texas","TX").replace("Utah","UT")\
                                                    .replace("Vermont","VT").replace("Virginia","VA").replace("Washington","WA")\
                                                        .replace("Wisconsin","WI").replace("Wyoming","WY").replace("All","USA")\
                                                            .replace("District of Columbia","DC").replace("SouthDakota","NC")\
                                                                .replace("NorthCarolina","NC").replace("Districtof Columbia","DC")
        allStates2.append(state)
    allStates2 = sorted(allStates2)
    return(",".join(allStates2))


#reformats dates from YYYY/M/D to YYYY-MM-DD
def ReformatDate(oldDate):
    odList = oldDate.split("/")
    #newDate = "-".join(odList)
    newDate = "%.4d-%.2d-%.2d" % (int(odList[0]), int(odList[1]), int(odList[2]))
    return(newDate)


#Converts the dictionary data to a reasonable output format and outputs it
def OutputData(dataDict, out):
    title = "uniqueID\tclade\tclusterID\tstates\tnumCases\tRR\tRcolor\tstartDate\tendDate\n"
    out.write(title)
    for clade, cladeData in dataDict.items():
        for cluster in cladeData.values():
            uniqueName = "%s_%s" % (clade, cluster[5])
            rColor = GetRcolor(cluster[2])
            newline = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (uniqueName, clade, cluster[5], cluster[0], cluster[1], cluster[2], rColor, cluster[3], cluster[4])
            out.write(newline)
            
#Generates R background colors from RR (relative risk) values
def GetRcolor(rr):
    #determine background color        
    if float(rr) < 8.0:
        col = "#FEF001"
    elif float(rr) < 15.0:
        col = "#FFB403"
    elif float(rr) < 21.0:
        col = "#fd6601"
    else:
        col = "red"
    
        
    return(col)




#Process input files and store data in dictionaries with the structure 
#  key: clade  val: region, cases, rr, startTime, stopTime
allDataDict = {}
IngestInput(inp_n1c1x, "N1.C.1.X", allDataDict)
IngestInput(inp_n1c2, "N1.C.2", allDataDict)
IngestInput(inp_n1c21, "N1.C.2.1", allDataDict)
IngestInput(inp_n1c3, "N1.C.3", allDataDict)
IngestInput(inp_n1c31, "N1.C.3.1", allDataDict)
IngestInput(inp_n1c32, "N1.C.3.2", allDataDict)
IngestInput(inp_n1p, "N1.P", allDataDict)


#Filter by rr and cases to make data subsets and add codes for multi-state groups
clusterIDdict = {} #a dict of key: cluster id val:state cluster
topIDnum = 1     #the number used to generate state cluster IDs
upDataDict = copy.deepcopy(allDataDict)
rr2DataDict = copy.deepcopy(allDataDict)
mostFiltDict = copy.deepcopy(allDataDict)
for clade, cladeData in allDataDict.items():
    for clusterNum, cluster in cladeData.items():
        #gather data
        rr = cluster[2]
        cas = cluster[1]
        states = cluster[0]
        
        #determine clusterID for clusters with more than one state or the USA
        if len(states.split(",")) > 1:
            if states in clusterIDdict:
                clusterID = clusterIDdict[states]
            else:
                clusterID = "SG%.2d" % (topIDnum)
                clusterIDdict[states] = clusterID
                
                newline = "%s\t%s\n" % (clusterID, states)
                out_stateID.write(newline)
                topIDnum += 1
        else:
            clusterID = states
            
            
        #add cluster ID
        allDataDict[clade][clusterNum].append(clusterID)
        upDataDict[clade][clusterNum].append(clusterID)
        rr2DataDict[clade][clusterNum].append(clusterID)
        mostFiltDict[clade][clusterNum].append(clusterID)

        #filter data to make up subset
        if float(rr) <= 1.0:
            upDataDict[clade].pop(clusterNum)
            rr2DataDict[clade].pop(clusterNum)
            mostFiltDict[clade].pop(clusterNum)
            
        elif float(rr) <= 2.0:
            rr2DataDict[clade].pop(clusterNum)
            mostFiltDict[clade].pop(clusterNum)
                
        elif int(cas) < 10:
            mostFiltDict[clade].pop(clusterNum)
                

#Go thorugh data subsets, convert to tabular format and output
OutputData(allDataDict, out_all)
OutputData(upDataDict, out_Up)
OutputData(rr2DataDict, out_Up_RR2)
OutputData(mostFiltDict, out_Up_RR2_cases10)















inp_n1c1x.close();inp_n1c2.close();inp_n1c21.close();inp_n1c3.close()
inp_n1c31.close();inp_n1c32.close();inp_n1p.close()
out_all.close();out_Up.close();out_Up_RR2_cases10.close()
out_Up_RR2.close();out_stateID.close()