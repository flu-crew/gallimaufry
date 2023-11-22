#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to take the updated versions of fasta files for OFFLU 
and to standardize all names
Created by David E. Hufnagel on Mon Jan 25 11:37:32 2021
"""
import sys

fdh3 = open("h3.fna")
fd1a = open("1A.fna")
fd1b = open("1B.fna")
fd1c = open("1C.fna")
h3Out = open("h3_Jan25.fna", "w")
h1Out = open("h1_Jan25.fna", "w")
h1aOut = open("1A_Jan25.fna", "w")
h1bOut = open("1B_Jan25.fna", "w")
h1cOut = open("1C_Jan25.fna", "w")



def ProcessInput(inpFD, out):
    for line in inpFD:
        if line.startswith(">"):
            if line.startswith(">Consensus"):
                out.write(line)
            else:
                lineLst = line.strip().strip(">").split("|")
                source = lineLst[0]; strain = lineLst[1]; subtype = lineLst[2]
                host = lineLst[3]; cntry = lineLst[4]
                
                if host != "Germany" and strain != "A/Hawaii/70/2019":
                    clade = lineLst[5]
                    date = lineLst[6]
                elif strain == "A/Hawaii/70/2019":
                    date = lineLst[-1]
                
                #check source
                ###test strains first
                if strain in ["A/swine/Italy/241572/2020", "A/swine/Spain/1297/2016", "A/swine/Spain/BM55/2019", \
                              "A/swine/Italy/185280/2020", "A/swine/Italy/64366/2020", "A/swine/Spain/007/2017", \
                                  "A/swine/Spain/BM54/2019", "A/swine/Italy/69273/2020", "A/swine/Italy/86554/2020", \
                                      "A/swine/Italy/127069/2020", "A/swine/Spain/BM38/2019", "A/swine/Spain/45690-10/2019", \
                                          "A/swine/Spain/090/2018", "A/swine/Italy/124375/2020", "A/swine/Illinois/A02524514/2020", \
                                              "A/swine/Alberta/SD0529/2020", "A/swine/Quebec/NCFAD-06-6/2020", \
                                                  "A/swine/Qubec/N-2020-3-24/2020", "A/swine/Minnesota/A02245409/2020", \
                                                      "A/swine/Minnesota/A02245409/2020", "A/swine/Illinois/A02139356/2018", \
                                                          "A/swine/Iowa/A02478968/2020", "A/swine/Iowa/A02524534/2020", \
                                                              "A/swine/Missouri/A02257614/2018", "A/swine/North_Carolina/A02245294/2019", \
                                                                  "A/swine/ON-N2019-40-3/2020", "A/swine/Quebec/N2020-6-4/2020", \
                                                                      "A/swine/Minnesota/A02245671/2020", "A/swine/Kansas/A02245675/2020", \
                                                                          "A/swine/Iowa/A02524572/2020"]:
                    if source in ["CAN-shipment", "offlu-vcm", "prevTest", "private"]:
                        source = "offlu-vcm|lab-21-a"
                    else:
                        source = "publicIAV|lab-21-a"
                else:
                    if not source in ["huReference", "huVaccine", "offlu-vcm", \
                                  "publicIAV", "syntheticIAV", "variant", "CVV"]: #good sources
                        if source in ["offlu", "private", "CAN-shipment", "prevTest"]:
                            source = "offlu-vcm|"
                        elif source == "ref":
                            source = "SwReference|"
                        else:
                            print("ERROR1 !")
                            sys.exit()
                    else:
                        source += "|"
                        
                #check strain
                if strain == "A/swine/Italy/A_swine_Italy_284922_2009_HA/2009":
                    strain = "A/swine/Italy/284922/2009"
                    
                #check subtype
                #  It's all good there
                
                if host == "swine":
                    host = "Swine"
                elif host == "human":
                    host = "Human"
                
                #check country
                if cntry == "human":
                    cntry = "USA"
                elif cntry[0] in ["1", "3"] and host != "Germany":
                    cntry = lineLst[5]
                    if cntry == "Spain":
                        cntry = "ESP"
                        
                #check clade
                if host != "Germany":
                    if clade == "2019-10-05" or clade == "human":
                        clade = "1A.3.3.2"
                    elif clade in ["CAN", "ITA", "Spain", "USA"]:
                        clade = lineLst[4]
                        if clade == "human":
                            clade  = "1A.3.3.2"
                
                #check date
                #  it's all good here by now
                
                #check host and fix one odd sequence
                if host == "Germany":
                    host = "Swine"
                    cntry = "DEU"
                    clade = lineLst[-1]
                    date = "1979"
                    
                    
                #Fix "Qubec" misspelling
                strain.replace("Qubec","Quebec")
                    
                newline = ">%s|%s|%s|%s|%s|%s|%s\n" % \
                    (source, strain, subtype, host, cntry, clade, date)
                out.write(newline)

        else:
            out.write(line)




ProcessInput(fdh3, h3Out)
ProcessInput(fd1a, h1aOut); fd1a.seek(0); ProcessInput(fd1a, h1Out)
ProcessInput(fd1b, h1bOut); fd1b.seek(0); ProcessInput(fd1b, h1Out)
ProcessInput(fd1c, h1cOut); fd1c.seek(0); ProcessInput(fd1c, h1Out)









fdh3.close()    
fd1a.close()
fd1b.close()    
fd1c.close()
h3Out.close()   
h1Out.close()
h1aOut.close()
h1bOut.close()       
h1cOut.close()   