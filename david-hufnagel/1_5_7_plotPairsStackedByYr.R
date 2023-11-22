library(ggplot2)
library(dplyr)
setwd("/Users/david.hufnagel/Documents/2_Research/1_2020/5_N1SelectionReborn/7_HApairing/2_10yrDataOverTime")


#import data
inp = read.table("pairData_10yr_RinpStacked_byYear.txt", sep="\t", header=TRUE)

#organize data
time <- inp$year                # x Axis
value <- inp$instance               # y Axis
group <- inp$haClade_naClade        # group, one shape per group
data <- data.frame(time, value, group)

#subset data
#goodLst excludes only "Other" and NA clades with only 1 HA pair
#goodLst3 also excludes clades with fewer than 30 sequences
goodLst3 = c("1A.3.3.3_N1.C.C.3", "1B.2.1_N1.C.C.3", "1A.3.3.3_N1.C.D.1", 
             "1B.2.2.1_N1.C.D.1", "1A.2_N1.C.D.2", "1A.3.3.2_N1.C.D.2", 
             "1A.3.3.3_N1.C.D.2", "1B.2.1_N1.C.D.2", "1A.3.3.3_N1.C.D.2.1", 
             "1B.2.1_N1.C.D.2.1", "1B.2.2.1_N1.C.D.2.1", "1B.2.2.2_N1.C.D.2.1", 
             "1A.3.3.2_N1.C.D.2.2", "1A.3.3.3_N1.C.D.2.2", "1A.1.1_N1.P", 
             "1A.2-3-like_N1.P", "1A.3.3.2_N1.P", "1A.3.3.3_N1.P", 
             "1B.2.1_N1.P", "1B.2.2.2_N1.P")

time4 <- subset(time, inp$haClade_naClade %in% goodLst3)
value4 <- subset(value, inp$haClade_naClade %in% goodLst3)
group4 <- subset(group, inp$haClade_naClade %in% goodLst3)
data4 = subset(data, inp$haClade_naClade %in% goodLst3)
subedInp = subset(inp, inp$haClade_naClade %in% goodLst3)

#plot data
plot.new()
pdf("nahaPairsOTstacked_10yrs_byYear.pdf", height=5.5, width=12)
ggplot(data4, aes(x=time4, y=value4, fill=group4)) + 
    geom_area() + labs(x="time", y="NA-HA pair occurances", fill="NA-HA pairs") + 
    ggtitle("NA-HA pairs of major NA clades over time") + 
    theme(plot.title=element_text(hjust=0.5)) + 
    scale_x_continuous(breaks=time4, label=as.character(time4))
    #scale_x_continuous(breaks=seq(3,129,3), label=as.character(seq(3,129,3)))
dev.off()


#Now do calculations for plotting percentages rather than totals
data5 = subedInp %>%
    group_by(year, haClade_naClade) %>%
    summarise(n = sum(instance)) %>%
    mutate(percentage = n / sum(n))

#Plot for percentages
plot.new()
pdf("nahaPairsOTstacked_10yrs_byYearPerc.pdf", height=5.5, width=12)
ggplot(data5, aes(x=year, y=percentage, fill=haClade_naClade)) +
    geom_area() + labs(x="time", y="HA-NA pair occurances", fill="HA-NA pairs") +
    ggtitle("HA-NA pairs of major NA clades over time") +
    theme(plot.title=element_text(hjust=0.5)) +
    scale_x_continuous(breaks=time4, label=as.character(time4))
dev.off()

#Plots split by N1.P & N1.E, N1.




