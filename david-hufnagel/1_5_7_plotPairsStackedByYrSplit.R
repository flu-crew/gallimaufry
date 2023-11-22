#This script is designed to create plots of HA-NA pairings over time in split
#by large (>=100inds) and small clades (<100inds)
#Created by David E. Hufnagel on Dec 2, 2020
library(ggplot2)
library(dplyr)
setwd("/Users/david.hufnagel/Documents/2_Research/1_2020/5_N1SelectionReborn/7_HApairing/2_10yrDataOverTime")


#import data
inpLarge = read.table("pairData_10yr_RinpStacked_byYear_splitLarge.txt", sep="\t", header=TRUE)
inpSmall = read.table("pairData_10yr_RinpStacked_byYear_splitSmall.txt", sep="\t", header=TRUE)

#organize data
timeL <- inpLarge$year                # x Axis
valueL <- inpLarge$instance               # y Axis
groupL <- inpLarge$haClade_naClade        # group, one shape per group
dataL <- data.frame(timeL, valueL, groupL)

timeS <- inpSmall$year                # x Axis
valueS <- inpSmall$instance               # y Axis
groupS <- inpSmall$haClade_naClade        # group, one shape per group
dataS <- data.frame(timeS, valueS, groupS)


#plot data
plot.new()
pdf("nahaPairsOTstacked_10yrs_byYearLarge.pdf", height=5.5, width=12)
ggplot(dataL, aes(x=timeL, y=valueL, fill=groupL)) + 
    geom_area() + labs(x="time", y="NA-HA pair occurances", fill="NA-HA pairs") + 
    ggtitle("NA-HA pairs of major NA clades over time") + 
    theme(plot.title=element_text(hjust=0.5)) + 
    scale_x_continuous(breaks=timeL, label=as.character(timeL))
dev.off()

plot.new()
pdf("nahaPairsOTstacked_10yrs_byYearSmall.pdf", height=5.5, width=12)
ggplot(dataS, aes(x=timeS, y=valueS, fill=groupS)) + 
    geom_area() + labs(x="time", y="NA-HA pair occurances", fill="NA-HA pairs") + 
    ggtitle("NA-HA pairs of major NA clades over time") + 
    theme(plot.title=element_text(hjust=0.5)) + 
    scale_x_continuous(breaks=timeS, label=as.character(timeS))
dev.off()


#Now do calculations for plotting percentages rather than totals
dataL2 = inpLarge %>%
    group_by(year, haClade_naClade) %>%
    summarise(n = sum(instance)) %>%
    mutate(percentage = n / sum(n))

dataS2 = inpSmall %>%
    group_by(year, haClade_naClade) %>%
    summarise(n = sum(instance)) %>%
    mutate(percentage = n / sum(n))


# Provide a set order
dataL2$haClade_naClade = 
    factor(dataL2$haClade_naClade, 
           levels=c("1A.3.3.3_N1.C.C.3","1B.2.1_N1.C.C.3","1A.3.3.3_N1.C.D.1",
                    "1B.2.2.1_N1.C.D.1","1A.2_N1.C.D.2","1A.3.2_N1.C.D.2",
                    "1A.3.3.3_N1.C.D.2","1B.2.1_N1.C.D.2","1A.3.3.3_N1.C.D.2.1",
                    "1B.2.1_N1.C.D.2.1","1B.2.2.1_N1.C.D.2.1","1B.2.2.2_N1.C.D.2.1",
                    "1A.3.3.2_N1.C.D.2.2","1A.3.3.3_N1.C.D.2.2","1A.1.1_N1.P",
                    "1A.2-3-like_N1.P","1A.3.3.2_N1.P","1A.3.3.3_N1.P",
                    "1B.2.1_N1.P","1B.2.2.2_N1.P"))
dataS2$haClade_naClade = 
    factor(dataS2$haClade_naClade, 
           levels=c("1A.1-like_N1.C.A","1A.1.1_N1.C.A", "1A.3.3.3_N1.C.A", 
                    "1A.2_N1.C.A.1", "1A.3.3.3_N1.C.A.1", "1A.2_N1.C.C",
                    "1A.3.3.3_N1.C.C", "1A.2_N1.C.D", "1A.3.3.2_N1.C.D", "1A.3.3.3_N1.C.D"))

#Plot for percentages
plot.new()
pdf("nahaPairsOTstacked_10yrs_byYearPerc_Large.pdf", height=5.5, width=12)
ggplot(dataL2, aes(x=year, y=percentage, fill=haClade_naClade)) +
    geom_area() + labs(x="time", y="HA-NA pair occurances", fill="HA-NA pairs") +
    ggtitle("HA-NA Pairs of Large NA Clades Over Time") +
    theme(plot.title=element_text(hjust=0.5)) +
    scale_x_continuous(breaks=timeL, label=as.character(timeL))
dev.off()

plot.new()
pdf("nahaPairsOTstacked_10yrs_byYearPerc_Small.pdf", height=5.5, width=12)
ggplot(dataS2, aes(x=year, y=percentage, fill=haClade_naClade)) +
    geom_area() + labs(x="time", y="HA-NA pair occurances", fill="HA-NA pairs") +
    ggtitle("HA-NA Pairs of Small NA Clades Over Time") +
    theme(plot.title=element_text(hjust=0.5)) +
    scale_x_continuous(breaks=timeS, label=as.character(timeS))
dev.off()






