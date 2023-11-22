#This script is designed to create plots of HA-NA pairings over time in split
#by each NA clade.
#Created by David E. Hufnagel on March 24, 2021
library(ggplot2)
library(dplyr)
setwd("/Users/david.hufnagel/Documents/2_Research/2_2021/1_N1project/3_AyrData/2_PairPlots")


#import data
inp = read.table("pairData_Ayr_RinpStacked_byYr.txt", sep="\t", header=TRUE)
inp_N1A = subset(inp, inp$naClade=="N1.A") 
inp_N1C = subset(inp, inp$naClade=="N1.C") 
inp_N1C1 = subset(inp, inp$naClade=="N1.C.1") 
inp_N1C11 = subset(inp, inp$naClade=="N1.C.1.1") 
inp_N1C12 = subset(inp, inp$naClade=="N1.C.1.2") 
inp_N1C2 = subset(inp, inp$naClade=="N1.C.2") 
inp_N1C21 = subset(inp, inp$naClade=="N1.C.2.1") 
inp_N1C3 = subset(inp, inp$naClade=="N1.C.3") 
inp_N1C31 = subset(inp, inp$naClade=="N1.C.3.1") 
inp_N1C32 = subset(inp, inp$naClade=="N1.C.3.2") 
inp_N1E = subset(inp, inp$naClade=="N1.E") 
inp_N1E1 = subset(inp, inp$naClade=="N1.E.1") 
inp_N1H = subset(inp, inp$naClade=="N1.H") 
inp_N1P = subset(inp, inp$naClade=="N1.P") 



#organize data
timeN1A <- inp_N1A$year                    # x Axis
valueN1A <- inp_N1A$instance               # y Axis
groupN1A <- inp_N1A$haClade_naClade        # group, one shape per group
data_N1A <- data.frame(timeN1A, valueN1A, groupN1A)

timeN1C <- inp_N1C$year                    # x Axis
valueN1C <- inp_N1C$instance               # y Axis
groupN1C <- inp_N1C$haClade_naClade        # group, one shape per group
data_N1C <- data.frame(timeN1C, valueN1C, groupN1C)

timeN1C1 <- inp_N1C1$year                    # x Axis
valueN1C1 <- inp_N1C1$instance               # y Axis
groupN1C1 <- inp_N1C1$haClade_naClade        # group, one shape per group
data_N1C1 <- data.frame(timeN1C1, valueN1C1, groupN1C1)

timeN1C11 <- inp_N1C11$year                    # x Axis
valueN1C11 <- inp_N1C11$instance               # y Axis
groupN1C11 <- inp_N1C11$haClade_naClade        # group, one shape per group
data_N1C11 <- data.frame(timeN1C11, valueN1C11, groupN1C11)

timeN1C12 <- inp_N1C12$year                    # x Axis
valueN1C12 <- inp_N1C12$instance               # y Axis
groupN1C12 <- inp_N1C12$haClade_naClade        # group, one shape per group
data_N1C12 <- data.frame(timeN1C12, valueN1C12, groupN1C12)

timeN1C2 <- inp_N1C2$year                    # x Axis
valueN1C2 <- inp_N1C2$instance               # y Axis
groupN1C2 <- inp_N1C2$haClade_naClade        # group, one shape per group
data_N1C2 <- data.frame(timeN1C2, valueN1C2, groupN1C2)

timeN1C21 <- inp_N1C21$year                    # x Axis
valueN1C21 <- inp_N1C21$instance               # y Axis
groupN1C21 <- inp_N1C21$haClade_naClade        # group, one shape per group
data_N1C21 <- data.frame(timeN1C21, valueN1C21, groupN1C21)

timeN1C3 <- inp_N1C3$year                    # x Axis
valueN1C3 <- inp_N1C3$instance               # y Axis
groupN1C3 <- inp_N1C3$haClade_naClade        # group, one shape per group
data_N1C3 <- data.frame(timeN1C3, valueN1C3, groupN1C3)

timeN1C31 <- inp_N1C31$year                    # x Axis
valueN1C31 <- inp_N1C31$instance               # y Axis
groupN1C31 <- inp_N1C31$haClade_naClade        # group, one shape per group
data_N1C31 <- data.frame(timeN1C31, valueN1C31, groupN1C31)

timeN1C32 <- inp_N1C32$year                    # x Axis
valueN1C32 <- inp_N1C32$instance               # y Axis
groupN1C32 <- inp_N1C32$haClade_naClade        # group, one shape per group
data_N1C32 <- data.frame(timeN1C32, valueN1C32, groupN1C32)

timeN1E <- inp_N1E$year                    # x Axis
valueN1E <- inp_N1E$instance               # y Axis
groupN1E <- inp_N1E$haClade_naClade        # group, one shape per group
data_N1E <- data.frame(timeN1E, valueN1E, groupN1E)

timeN1E1 <- inp_N1E1$year                    # x Axis
valueN1E1 <- inp_N1E1$instance               # y Axis
groupN1E1 <- inp_N1E1$haClade_naClade        # group, one shape per group
data_N1E1 <- data.frame(timeN1E1, valueN1E1, groupN1E1)

timeN1H <- inp_N1H$year                    # x Axis
valueN1H <- inp_N1H$instance               # y Axis
groupN1H <- inp_N1H$haClade_naClade        # group, one shape per group
data_N1H <- data.frame(timeN1H, valueN1H, groupN1H)

timeN1P <- inp_N1P$year                    # x Axis
valueN1P <- inp_N1P$instance               # y Axis
groupN1P <- inp_N1P$haClade_naClade        # group, one shape per group
data_N1P <- data.frame(timeN1P, valueN1P, groupN1P)



#plot data
# plot.new()
# pdf("pairPlotCnts_Ayr_N1A.pdf", height=5.5, width=12)
# ggplot(data_N1A, aes(x=timeN1A, y=valueN1A, fill=groupN1A)) + 
#     geom_area() + labs(x="time", y="NA-HA pair occurances", fill="NA-HA pairs") + 
#     ggtitle("NA-HA pairs of N1.A strains over time") + 
#     theme(plot.title=element_text(hjust=0.5)) + 
#     scale_x_continuous(breaks=timeN1A, label=as.character(timeN1A))
# dev.off()

plot.new()
pdf("pairPlotCnts_Ayr_N1C.pdf", height=4.5, width=12)
ggplot(data_N1C, aes(x=timeN1C, y=valueN1C, fill=groupN1C)) + 
    geom_area() + labs(x="time", y="NA-HA pair occurances", fill="NA-HA pairs") + 
    ggtitle("NA-HA pairs of N1.C strains over time") + 
    theme(plot.title=element_text(hjust=0.5)) + 
    scale_x_continuous(breaks=timeN1C, label=as.character(timeN1C), limits=c(1930, 2020)) +
    theme(axis.text.x = element_text(angle = 90, size = 8))
dev.off()

plot.new()
pdf("pairPlotCnts_Ayr_N1C1.pdf", height=4.5, width=12)
ggplot(data_N1C1, aes(x=timeN1C1, y=valueN1C1, fill=groupN1C1)) + 
    geom_area() + labs(x="time", y="NA-HA pair occurances", fill="NA-HA pairs") + 
    ggtitle("NA-HA pairs of N1.C.1 strains over time") + 
    theme(plot.title=element_text(hjust=0.5)) + 
    scale_x_continuous(breaks=timeN1C1, label=as.character(timeN1C1), limits=c(1987, 2020)) +
    theme(axis.text.x = element_text(angle = 90, size = 8))
dev.off()

# plot.new()
# pdf("pairPlotCnts_Ayr_N1C11.pdf", height=5.5, width=12)
# ggplot(data_N1C11, aes(x=timeN1C11, y=valueN1C11, fill=groupN1C11)) + 
#     geom_area() + labs(x="time", y="NA-HA pair occurances", fill="NA-HA pairs") + 
#     ggtitle("NA-HA pairs of N1.C.1.1 strains over time") + 
#     theme(plot.title=element_text(hjust=0.5)) + 
#     scale_x_continuous(breaks=timeN1C11, label=as.character(timeN1C11), limits=c(1998, 2020)) +
#     theme(axis.text.x = element_text(angle = 90, size = 8))
# dev.off()

plot.new()
pdf("pairPlotCnts_Ayr_N1C12.pdf", height=4.5, width=12)
ggplot(data_N1C12, aes(x=timeN1C12, y=valueN1C12, fill=groupN1C12)) + 
    geom_area() + labs(x="time", y="NA-HA pair occurances", fill="NA-HA pairs") + 
    ggtitle("NA-HA pairs of N1.C.1.2 strains over time") + 
    theme(plot.title=element_text(hjust=0.5)) + 
    scale_x_continuous(breaks=timeN1C12, label=as.character(timeN1C12), limits=c(1999, 2020)) +
    theme(axis.text.x = element_text(angle = 90, size = 8))
dev.off()

plot.new()
pdf("pairPlotCnts_Ayr_N1C2.pdf", height=4.5, width=12)
ggplot(data_N1C2, aes(x=timeN1C2, y=valueN1C2, fill=groupN1C2)) + 
    geom_area() + labs(x="time", y="NA-HA pair occurances", fill="NA-HA pairs") + 
    ggtitle("NA-HA pairs of N1.C.2 strains over time") + 
    theme(plot.title=element_text(hjust=0.5)) + 
    scale_x_continuous(breaks=timeN1C2, label=as.character(timeN1C2), limits=c(2003, 2020)) +
    theme(axis.text.x = element_text(angle = 90, size = 8))
dev.off()

plot.new()
pdf("pairPlotCnts_Ayr_N1C21.pdf", height=4.5, width=12)
ggplot(data_N1C21, aes(x=timeN1C21, y=valueN1C21, fill=groupN1C21)) + 
    geom_area() + labs(x="time", y="NA-HA pair occurances", fill="NA-HA pairs") + 
    ggtitle("NA-HA pairs of N1.C.2.1 strains over time") + 
    theme(plot.title=element_text(hjust=0.5)) + 
    scale_x_continuous(breaks=timeN1C21, label=as.character(timeN1C21), limits=c(2006, 2020)) +
    theme(axis.text.x = element_text(angle = 90, size = 8))
dev.off()

plot.new()
pdf("pairPlotCnts_Ayr_N1C3.pdf", height=4.5, width=12)
ggplot(data_N1C3, aes(x=timeN1C3, y=valueN1C3, fill=groupN1C3)) + 
    geom_area() + labs(x="time", y="NA-HA pair occurances", fill="NA-HA pairs") + 
    ggtitle("NA-HA pairs of N1.C.3 strains over time") + 
    theme(plot.title=element_text(hjust=0.5)) + 
    scale_x_continuous(breaks=timeN1C3, label=as.character(timeN1C3), limits=c(2001, 2020)) +
    theme(axis.text.x = element_text(angle = 90, size = 8))
dev.off()

plot.new()
pdf("pairPlotCnts_Ayr_N1C31.pdf", height=4.5, width=12)
ggplot(data_N1C31, aes(x=timeN1C31, y=valueN1C31, fill=groupN1C31)) + 
    geom_area() + labs(x="time", y="NA-HA pair occurances", fill="NA-HA pairs") + 
    ggtitle("NA-HA pairs of N1.C.3.1 strains over time") + 
    theme(plot.title=element_text(hjust=0.5)) + 
    scale_x_continuous(breaks=timeN1C31, label=as.character(timeN1C31), limits=c(2011, 2020)) +
    theme(axis.text.x = element_text(angle = 90, size = 8))
dev.off()

plot.new()
pdf("pairPlotCnts_Ayr_N1C32.pdf", height=4.5, width=12)
ggplot(data_N1C32, aes(x=timeN1C32, y=valueN1C32, fill=groupN1C32)) + 
    geom_area() + labs(x="time", y="NA-HA pair occurances", fill="NA-HA pairs") + 
    ggtitle("NA-HA pairs of N1.C.3.2 strains over time") + 
    theme(plot.title=element_text(hjust=0.5)) + 
    scale_x_continuous(breaks=timeN1C32, label=as.character(timeN1C32), limits=c(2012, 2020)) +
    theme(axis.text.x = element_text(angle = 90, size = 8))
dev.off()

# plot.new()
# pdf("pairPlotCnts_Ayr_N1E.pdf", height=5.5, width=12)
# ggplot(data_N1E, aes(x=timeN1E, y=valueN1E, fill=groupN1E)) + 
#     geom_area() + labs(x="time", y="NA-HA pair occurances", fill="NA-HA pairs") + 
#     ggtitle("NA-HA pairs of N1.E strains over time") + 
#     theme(plot.title=element_text(hjust=0.5)) + 
#     scale_x_continuous(breaks=timeN1E, label=as.character(timeN1E), limits=c(2012, 2014)) +
#     theme(axis.text.x = element_text(angle = 90, size = 8))
# dev.off()

# plot.new()
# pdf("pairPlotCnts_Ayr_N1E1.pdf", height=5.5, width=12)
# ggplot(data_N1E1, aes(x=timeN1E1, y=valueN1E1, fill=groupN1E1)) + 
#     geom_area() + labs(x="time", y="NA-HA pair occurances", fill="NA-HA pairs") + 
#     ggtitle("NA-HA pairs of N1.E.1 strains over time") + 
#     theme(plot.title=element_text(hjust=0.5)) + 
#     scale_x_continuous(breaks=timeN1E1, label=as.character(timeN1E1), limits=c(1930, 2020)) +
#     theme(axis.text.x = element_text(angle = 90, size = 8))
# dev.off()

plot.new()
pdf("pairPlotCnts_Ayr_N1H.pdf", height=4.5, width=12)
ggplot(data_N1H, aes(x=timeN1H, y=valueN1H, fill=groupN1H)) + 
    geom_area() + labs(x="time", y="NA-HA pair occurances", fill="NA-HA pairs") + 
    ggtitle("NA-HA pairs of N1.H strains over time") + 
    theme(plot.title=element_text(hjust=0.5)) + 
    scale_x_continuous(breaks=timeN1H, label=as.character(timeN1H), limits=c(2004, 2010)) +
    theme(axis.text.x = element_text(angle = 90, size = 8))
dev.off()

plot.new()
pdf("pairPlotCnts_Ayr_N1P.pdf", height=4.5, width=12)
ggplot(data_N1P, aes(x=timeN1P, y=valueN1P, fill=groupN1P)) + 
    geom_area() + labs(x="time", y="NA-HA pair occurances", fill="NA-HA pairs") + 
    ggtitle("NA-HA pairs of N1.P strains over time") + 
    theme(plot.title=element_text(hjust=0.5)) + 
    scale_x_continuous(breaks=timeN1P, label=as.character(timeN1P), limits=c(2008, 2020)) +
    theme(axis.text.x = element_text(angle = 90, size = 8))
dev.off()



#Prepare to plot data by percentage
data2_N1C = inp_N1C %>%
    group_by(year, haClade_naClade) %>%
    summarise(n = sum(instance)) %>%
    mutate(percentage = n / sum(n))

data2_N1C1 = inp_N1C1 %>%
    group_by(year, haClade_naClade) %>%
    summarise(n = sum(instance)) %>%
    mutate(percentage = n / sum(n))

data2_N1C2 = inp_N1C2 %>%
    group_by(year, haClade_naClade) %>%
    summarise(n = sum(instance)) %>%
    mutate(percentage = n / sum(n))

data2_N1C3 = inp_N1C3 %>%
    group_by(year, haClade_naClade) %>%
    summarise(n = sum(instance)) %>%
    mutate(percentage = n / sum(n))

data2_N1C12 = inp_N1C12 %>%
    group_by(year, haClade_naClade) %>%
    summarise(n = sum(instance)) %>%
    mutate(percentage = n / sum(n))

data2_N1C21 = inp_N1C21 %>%
    group_by(year, haClade_naClade) %>%
    summarise(n = sum(instance)) %>%
    mutate(percentage = n / sum(n))

data2_N1C31 = inp_N1C31 %>%
    group_by(year, haClade_naClade) %>%
    summarise(n = sum(instance)) %>%
    mutate(percentage = n / sum(n))

data2_N1C32 = inp_N1C32 %>%
    group_by(year, haClade_naClade) %>%
    summarise(n = sum(instance)) %>%
    mutate(percentage = n / sum(n))

data2_N1H = inp_N1H %>%
    group_by(year, haClade_naClade) %>%
    summarise(n = sum(instance)) %>%
    mutate(percentage = n / sum(n))

data2_N1P = inp_N1P %>%
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
pdf("pairPlotPerc_Ayrs_N1C.pdf", height=4.5, width=12)
ggplot(data2_N1C, aes(x=year, y=percentage, fill=haClade_naClade)) +
    geom_area() + labs(x="time", y="HA-NA pair occurances", fill="HA-NA pairs") +
    ggtitle("HA-NA Pairs for strains within N1.C over time") +
    theme(plot.title=element_text(hjust=0.5)) +
    scale_x_continuous(breaks=timeN1C, label=as.character(timeN1C), limits=c(1930, 2020)) +
    theme(axis.text.x = element_text(angle = 90, size = 8))
dev.off()

plot.new()
pdf("pairPlotPerc_Ayrs_N1C1.pdf", height=4.5, width=12)
ggplot(data2_N1C1, aes(x=year, y=percentage, fill=haClade_naClade)) +
    geom_area() + labs(x="time", y="HA-NA pair occurances", fill="HA-NA pairs") +
    ggtitle("HA-NA Pairs for strains within N1.C.1 over time") +
    theme(plot.title=element_text(hjust=0.5)) +
    scale_x_continuous(breaks=timeN1C1, label=as.character(timeN1C1), limits=c(1987, 2020)) +
    theme(axis.text.x = element_text(angle = 90, size = 8))
dev.off()
    
plot.new()
pdf("pairPlotPerc_Ayrs_N1C2.pdf", height=4.5, width=12)
ggplot(data2_N1C2, aes(x=year, y=percentage, fill=haClade_naClade)) +
    geom_area() + labs(x="time", y="HA-NA pair occurances", fill="HA-NA pairs") +
    ggtitle("HA-NA Pairs for strains within N1.C.2 over time") +
    theme(plot.title=element_text(hjust=0.5)) +
    scale_x_continuous(breaks=timeN1C2, label=as.character(timeN1C2), limits=c(2003, 2020)) +
    theme(axis.text.x = element_text(angle = 90, size = 8))
dev.off()

plot.new()
pdf("pairPlotPerc_Ayrs_N1C3.pdf", height=4.5, width=12)
ggplot(data2_N1C3, aes(x=year, y=percentage, fill=haClade_naClade)) +
    geom_area() + labs(x="time", y="HA-NA pair occurances", fill="HA-NA pairs") +
    ggtitle("HA-NA Pairs for strains within N1.C.3 over time") +
    theme(plot.title=element_text(hjust=0.5)) +
    scale_x_continuous(breaks=timeN1C3, label=as.character(timeN1C3), limits=c(2001, 2020)) +
    theme(axis.text.x = element_text(angle = 90, size = 8))
dev.off()

plot.new()
pdf("pairPlotPerc_Ayrs_N1C12.pdf", height=4.5, width=12)
ggplot(data2_N1C12, aes(x=year, y=percentage, fill=haClade_naClade)) +
    geom_area() + labs(x="time", y="HA-NA pair occurances", fill="HA-NA pairs") +
    ggtitle("HA-NA Pairs for strains within N1.C.1.2 over time") +
    theme(plot.title=element_text(hjust=0.5)) +
    scale_x_continuous(breaks=timeN1C12, label=as.character(timeN1C12), limits=c(1999, 2020)) +
    theme(axis.text.x = element_text(angle = 90, size = 8))
dev.off()

plot.new()
pdf("pairPlotPerc_Ayrs_N1C21.pdf", height=4.5, width=12)
ggplot(data2_N1C21, aes(x=year, y=percentage, fill=haClade_naClade)) +
    geom_area() + labs(x="time", y="HA-NA pair occurances", fill="HA-NA pairs") +
    ggtitle("HA-NA Pairs for strains within N1.C.2.1 over time") +
    theme(plot.title=element_text(hjust=0.5)) +
    scale_x_continuous(breaks=timeN1C21, label=as.character(timeN1C21), limits=c(2006, 2020)) +
    theme(axis.text.x = element_text(angle = 90, size = 8))
dev.off()

plot.new()
pdf("pairPlotPerc_Ayrs_N1C31.pdf", height=4.5, width=12)
ggplot(data2_N1C31, aes(x=year, y=percentage, fill=haClade_naClade)) +
    geom_area() + labs(x="time", y="HA-NA pair occurances", fill="HA-NA pairs") +
    ggtitle("HA-NA Pairs for strains within N1.C.3.1 over time") +
    theme(plot.title=element_text(hjust=0.5)) +
    scale_x_continuous(breaks=timeN1C31, label=as.character(timeN1C31), limits=c(2011, 2020)) +
    theme(axis.text.x = element_text(angle = 90, size = 8))
dev.off()

plot.new()
pdf("pairPlotPerc_Ayrs_N1C32.pdf", height=4.5, width=12)
ggplot(data2_N1C32, aes(x=year, y=percentage, fill=haClade_naClade)) +
    geom_area() + labs(x="time", y="HA-NA pair occurances", fill="HA-NA pairs") +
    ggtitle("HA-NA Pairs for strains within N1.C.3.2 over time") +
    theme(plot.title=element_text(hjust=0.5)) +
    scale_x_continuous(breaks=timeN1C32, label=as.character(timeN1C32), limits=c(2012, 2020)) +
    theme(axis.text.x = element_text(angle = 90, size = 8))
dev.off()

plot.new()
pdf("pairPlotPerc_Ayrs_N1H.pdf", height=4.5, width=12)
ggplot(data2_N1H, aes(x=year, y=percentage, fill=haClade_naClade)) +
    geom_area() + labs(x="time", y="HA-NA pair occurances", fill="HA-NA pairs") +
    ggtitle("HA-NA Pairs for strains within N1.H over time") +
    theme(plot.title=element_text(hjust=0.5)) +
    scale_x_continuous(breaks=timeN1H, label=as.character(timeN1H), limits=c(2004, 2010)) +
    theme(axis.text.x = element_text(angle = 90, size = 8))
dev.off()

plot.new()
pdf("pairPlotPerc_Ayrs_N1P.pdf", height=4.5, width=12)
ggplot(data2_N1P, aes(x=year, y=percentage, fill=haClade_naClade)) +
    geom_area() + labs(x="time", y="HA-NA pair occurances", fill="HA-NA pairs") +
    ggtitle("HA-NA Pairs for strains within N1.P over time") +
    theme(plot.title=element_text(hjust=0.5)) +
    scale_x_continuous(breaks=timeN1P, label=as.character(timeN1P), limits=c(2008, 2020)) +
    theme(axis.text.x = element_text(angle = 90, size = 8))
dev.off()





