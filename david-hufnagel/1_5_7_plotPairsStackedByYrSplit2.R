#This script is designed to create plots of HA-NA pairings over time in split
#by large (>=100inds) and small clades (<100inds)
#Created by David E. Hufnagel on Dec 2, 2020
#This version created on Jan 8, 2021 is meant for data split into separate
#   files by region
library(ggplot2)
library(dplyr)
setwd("/Users/david.hufnagel/Documents/2_Research/2_2021/1_N1project/2_10ryData/1_PairGraphsByRegion/")


#import data
inp1 = read.table("pairData_10yr_RinpStacked_byYear_1.txt", sep="\t", header=TRUE)
inp2 = read.table("pairData_10yr_RinpStacked_byYear_2.txt", sep="\t", header=TRUE)
inp3 = read.table("pairData_10yr_RinpStacked_byYear_3.txt", sep="\t", header=TRUE)
inp4 = read.table("pairData_10yr_RinpStacked_byYear_4.txt", sep="\t", header=TRUE)
inp5 = read.table("pairData_10yr_RinpStacked_byYear_5.txt", sep="\t", header=TRUE)
inpCAN = read.table("pairData_10yr_RinpStacked_byYear_CAN.txt", sep="\t", header=TRUE)
inpMEX = read.table("pairData_10yr_RinpStacked_byYear_MEX.txt", sep="\t", header=TRUE)
inpN1CA = read.table("pairData_10yr_RinpStacked_byYear_allReg_N1.C.A.txt", sep="\t", header=TRUE)
inpN1CC = read.table("pairData_10yr_RinpStacked_byYear_allReg_N1.C.C.txt", sep="\t", header=TRUE)
inpN1CD = read.table("pairData_10yr_RinpStacked_byYear_allReg_N1.C.D.txt", sep="\t", header=TRUE)
inpN1P = read.table("pairData_10yr_RinpStacked_byYear_allReg_N1.P.txt", sep="\t", header=TRUE)


#organize data
time1 <- inp1$year                    # x Axis
value1 <- inp1$instance               # y Axis
group1 <- inp1$haClade_naClade        # group, one shape per group
data1 <- data.frame(time1, value1, group1)

time2 <- inp2$year                    # x Axis
value2 <- inp2$instance               # y Axis
group2 <- inp2$haClade_naClade        # group, one shape per group
data2 <- data.frame(time2, value2, group2)

time3 <- inp3$year                    # x Axis
value3 <- inp3$instance               # y Axis
group3 <- inp3$haClade_naClade        # group, one shape per group
data3 <- data.frame(time3, value3, group3)

time4 <- inp4$year                    # x Axis
value4 <- inp4$instance               # y Axis
group4 <- inp4$haClade_naClade        # group, one shape per group
data4 <- data.frame(time4, value4, group4)

time5 <- inp5$year                    # x Axis
value5 <- inp5$instance               # y Axis
group5 <- inp5$haClade_naClade        # group, one shape per group
data5 <- data.frame(time5, value5, group5)

timeC <- inpCAN$year                    # x Axis
valueC <- inpCAN$instance               # y Axis
groupC <- inpCAN$haClade_naClade        # group, one shape per group
dataC <- data.frame(timeC, valueC, groupC)

timeM <- inpMEX$year                    # x Axis
valueM <- inpMEX$instance               # y Axis
groupM <- inpMEX$haClade_naClade        # group, one shape per group
dataM <- data.frame(timeM, valueM, groupM)

timeN1CA <- inpN1CA$year                    # x Axis
valueN1CA <- inpN1CA$instance               # y Axis
groupN1CA <- inpN1CA$haClade_naClade        # group, one shape per group
dataN1CA <- data.frame(timeN1CA, valueN1CA, groupN1CA)

timeN1CC <- inpN1CC$year                    # x Axis
valueN1CC <- inpN1CC$instance               # y Axis
groupN1CC <- inpN1CC$haClade_naClade        # group, one shape per group
dataN1CC <- data.frame(timeN1CC, valueN1CC, groupN1CC)

timeN1CD <- inpN1CA$year                    # x Axis
valueN1CD <- inpN1CA$instance               # y Axis
groupN1CD <- inpN1CA$haClade_naClade        # group, one shape per group
dataN1CD <- data.frame(timeN1CD, valueN1CD, groupN1CD)

timeN1P <- inpN1P$year                    # x Axis
valueN1P <- inpN1P$instance               # y Axis
groupN1P <- inpN1P$haClade_naClade        # group, one shape per group
dataN1P <- data.frame(timeN1P, valueN1P, groupN1P)


#Prepare to plot data by percentage
data1_2 = inp1 %>%
    group_by(year, haClade_naClade) %>%
    summarise(n = sum(instance)) %>%
    mutate(percentage = n / sum(n))

data2_2 = inp2 %>%
    group_by(year, haClade_naClade) %>%
    summarise(n = sum(instance)) %>%
    mutate(percentage = n / sum(n))

data3_2 = inp3 %>%
    group_by(year, haClade_naClade) %>%
    summarise(n = sum(instance)) %>%
    mutate(percentage = n / sum(n))

data4_2 = inp4 %>%
    group_by(year, haClade_naClade) %>%
    summarise(n = sum(instance)) %>%
    mutate(percentage = n / sum(n))

data5_2 = inp5 %>%
    group_by(year, haClade_naClade) %>%
    summarise(n = sum(instance)) %>%
    mutate(percentage = n / sum(n))

dataC_2 = inpCAN %>%
    group_by(year, haClade_naClade) %>%
    summarise(n = sum(instance)) %>%
    mutate(percentage = n / sum(n))

dataM_2 = inpMEX %>%
    group_by(year, haClade_naClade) %>%
    summarise(n = sum(instance)) %>%
    mutate(percentage = n / sum(n))

dataN1CA_2 = inpN1CA %>%
    group_by(year, haClade_naClade) %>%
    summarise(n = sum(instance)) %>%
    mutate(percentage = n / sum(n))

dataN1CC_2 = inpN1CC %>%
    group_by(year, haClade_naClade) %>%
    summarise(n = sum(instance)) %>%
    mutate(percentage = n / sum(n))

dataN1CD_2 = inpN1CD %>%
    group_by(year, haClade_naClade) %>%
    summarise(n = sum(instance)) %>%
    mutate(percentage = n / sum(n))

dataN1P_2 = inpN1P %>%
    group_by(year, haClade_naClade) %>%
    summarise(n = sum(instance)) %>%
    mutate(percentage = n / sum(n))


#Provide a set order for all regions plots
# dataL2$haClade_naClade = 
#     factor(dataL2$haClade_naClade, 
#            levels=c("1A.3.3.3_N1.C.C.3","1B.2.1_N1.C.C.3","1A.3.3.3_N1.C.D.1",
#                     "1B.2.2.1_N1.C.D.1","1A.2_N1.C.D.2","1A.3.2_N1.C.D.2",
#                     "1A.3.3.3_N1.C.D.2","1B.2.1_N1.C.D.2","1A.3.3.3_N1.C.D.2.1",
#                     "1B.2.1_N1.C.D.2.1","1B.2.2.1_N1.C.D.2.1","1B.2.2.2_N1.C.D.2.1",
#                     "1A.3.3.2_N1.C.D.2.2","1A.3.3.3_N1.C.D.2.2","1A.1.1_N1.P",
#                     "1A.2-3-like_N1.P","1A.3.3.2_N1.P","1A.3.3.3_N1.P",
#                     "1B.2.1_N1.P","1B.2.2.2_N1.P"))
# dataS2$haClade_naClade = 
#     factor(dataS2$haClade_naClade, 
#            levels=c("1A.1-like_N1.C.A","1A.1.1_N1.C.A", "1A.3.3.3_N1.C.A", 
#                     "1A.2_N1.C.A.1", "1A.3.3.3_N1.C.A.1", "1A.2_N1.C.C",
#                     "1A.3.3.3_N1.C.C", "1A.2_N1.C.D", "1A.3.3.2_N1.C.D", "1A.3.3.3_N1.C.D"))




#Plot by percentages for each region and all clades
plot.new()
pdf("nahaPairsOT_10yrs_byYearPerc_Reg1.pdf", height=5.5, width=12)
ggplot(data1_2, aes(x=year, y=percentage, fill=haClade_naClade)) +
    geom_area() + labs(x="time", y="HA-NA pair occurances", fill="HA-NA pairs") +
    ggtitle("HA-NA Pairs of NA Clades in USA Region 1 Over Time") +
    theme(plot.title=element_text(hjust=0.5)) +
    scale_x_continuous(breaks=time1, label=as.character(time1))
dev.off()

plot.new()
pdf("nahaPairsOT_10yrs_byYearPerc_Reg2.pdf", height=5.5, width=12)
ggplot(data2_2, aes(x=year, y=percentage, fill=haClade_naClade)) +
    geom_area() + labs(x="time", y="HA-NA pair occurances", fill="HA-NA pairs") +
    ggtitle("HA-NA Pairs of NA Clades in USA Region 2 Over Time") +
    theme(plot.title=element_text(hjust=0.5)) +
    scale_x_continuous(breaks=time2, label=as.character(time2))
dev.off()

plot.new()
pdf("nahaPairsOT_10yrs_byYearPerc_Reg3.pdf", height=5.5, width=12)
ggplot(data3_2, aes(x=year, y=percentage, fill=haClade_naClade)) +
    geom_area() + labs(x="time", y="HA-NA pair occurances", fill="HA-NA pairs") +
    ggtitle("HA-NA Pairs of NA Clades in USA Region 3 Over Time") +
    theme(plot.title=element_text(hjust=0.5)) +
    scale_x_continuous(breaks=time3, label=as.character(time3))
dev.off()

plot.new()
pdf("nahaPairsOT_10yrs_byYearPerc_Reg4.pdf", height=5.5, width=12)
ggplot(data4_2, aes(x=year, y=percentage, fill=haClade_naClade)) +
    geom_area() + labs(x="time", y="HA-NA pair occurances", fill="HA-NA pairs") +
    ggtitle("HA-NA Pairs of NA Clades in USA Region 4 Over Time") +
    theme(plot.title=element_text(hjust=0.5)) +
    scale_x_continuous(breaks=time4, label=as.character(time4))
dev.off()

plot.new()
pdf("nahaPairsOT_10yrs_byYearPerc_Reg5.pdf", height=5.5, width=12)
ggplot(data5_2, aes(x=year, y=percentage, fill=haClade_naClade)) +
    geom_area() + labs(x="time", y="HA-NA pair occurances", fill="HA-NA pairs") +
    ggtitle("HA-NA Pairs of NA Clades in USA Region 5 Over Time") +
    theme(plot.title=element_text(hjust=0.5)) +
    scale_x_continuous(breaks=time5, label=as.character(time5))
dev.off()

plot.new()
pdf("nahaPairsOT_10yrs_byYearPerc_RegC.pdf", height=5.5, width=12)
ggplot(dataC_2, aes(x=year, y=percentage, fill=haClade_naClade)) +
    geom_area() + labs(x="time", y="HA-NA pair occurances", fill="HA-NA pairs") +
    ggtitle("HA-NA Pairs of NA Clades in Canada Over Time") +
    theme(plot.title=element_text(hjust=0.5)) +
    scale_x_continuous(breaks=timeC, label=as.character(timeC))
dev.off()

plot.new()
pdf("nahaPairsOT_10yrs_byYearPerc_RegM.pdf", height=5.5, width=12)
ggplot(dataM_2, aes(x=year, y=percentage, fill=haClade_naClade)) +
    geom_area() + labs(x="time", y="HA-NA pair occurances", fill="HA-NA pairs") +
    ggtitle("HA-NA Pairs of NA Clades in Mexico Over Time") +
    theme(plot.title=element_text(hjust=0.5)) +
    scale_x_continuous(breaks=timeM, label=as.character(timeM))
dev.off()

plot.new()
pdf("nahaPairsOT_10yrs_byYearPerc_RegN1CA.pdf", height=5.5, width=12)
ggplot(dataN1CA_2, aes(x=year, y=percentage, fill=haClade_naClade)) +
    geom_area() + labs(x="time", y="HA-NA pair occurances", fill="HA-NA pairs") +
    ggtitle("HA-NA Pairs of N1.C.A NA Clades Over Time") +
    theme(plot.title=element_text(hjust=0.5)) +
    scale_x_continuous(breaks=timeN1CA, label=as.character(timeN1CA))
dev.off()

plot.new()
pdf("nahaPairsOT_10yrs_byYearPerc_RegN1CC.pdf", height=5.5, width=12)
ggplot(dataN1CC_2, aes(x=year, y=percentage, fill=haClade_naClade)) +
    geom_area() + labs(x="time", y="HA-NA pair occurances", fill="HA-NA pairs") +
    ggtitle("HA-NA Pairs of N1.C.C NA Clades Over Time") +
    theme(plot.title=element_text(hjust=0.5)) +
    scale_x_continuous(breaks=timeN1CC, label=as.character(timeN1CC))
dev.off()

plot.new()
pdf("nahaPairsOT_10yrs_byYearPerc_RegN1CD.pdf", height=5.5, width=12)
ggplot(dataN1CD_2, aes(x=year, y=percentage, fill=haClade_naClade)) +
    geom_area() + labs(x="time", y="HA-NA pair occurances", fill="HA-NA pairs") +
    ggtitle("HA-NA Pairs of N1.C.D NA Clades Over Time") +
    theme(plot.title=element_text(hjust=0.5)) +
    scale_x_continuous(breaks=timeN1CD, label=as.character(timeN1CD))
dev.off()

plot.new()
pdf("nahaPairsOT_10yrs_byYearPerc_RegN1P.pdf", height=5.5, width=12)
ggplot(dataN1P_2, aes(x=year, y=percentage, fill=haClade_naClade)) +
    geom_area() + labs(x="time", y="HA-NA pair occurances", fill="HA-NA pairs") +
    ggtitle("HA-NA Pairs of N1.P NA Clades Over Time") +
    theme(plot.title=element_text(hjust=0.5)) +
    scale_x_continuous(breaks=timeN1P, label=as.character(timeN1P))
dev.off()







