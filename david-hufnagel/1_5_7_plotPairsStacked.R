library(ggplot2)
library(dplyr)
setwd("/Users/david.hufnagel/Documents/2_Research/1_2020/5_N1SelectionReborn/7_HApairing/2_10yrDataOverTime")


#import data
inp = read.table("pairData_10yr_RinpStacked.txt", sep="\t", header=TRUE)

#organize data
time <- inp$monthNum                # x Axis
value <- inp$instance               # y Axis
group <- inp$naClade_haClade        # group, one shape per group
data <- data.frame(time, value, group)

#subset data
#goodLst excludes only "Other" and NA clades with only 1 HA pair
# goodLst = c("N1.C.A_1A.1-like","N1.C.A_1A.1.1", "N1.C.A_1A.3.3.3", 
#             "N1.C.A.1_1A.2", "N1.C.A.1_1A.3.3.3", "N1.C.C_1A.2", 
#             "N1.C.C_1A.3.3.3", "N1.C.C.3_1A.3.3.3", "N1.C.C.3_1B.2.1", 
#             "N1.C.D_1A.2", "N1.C.D_1A.3.3.2", "N1.C.D_1A.3.3.3", 
#             "N1.C.D.1_1A.3.3.3", "N1.C.D.1_1B.2.2.1", "N1.C.D.2_1A.2", 
#             "N1.C.D.2_1A.3.2", "N1.C.D.2_1A.3.3.3", "N1.C.D.2_1B.2.1",
#             "N1.C.D.2.1_1A.3.3.3", "N1.C.D.2.1_1B.2.1", "N1.C.D.2.1_1B.2.2.1", 
#             "N1.C.D.2.1_1B.2.2.2", "1.C.D.2.2_1A.3.3.2", "N1.C.D.2.2_1A.3.3.3", 
#             "N1.P_1A.1.1", "N1.P_1A.2-3-like", "N1.P_1A.3.3.2", "N1.P_1A.3.3.3", 
#             "N1.P_1B.2.1", "N1.P_1B.2.2.2")
# time2 <- subset(time, inp$naClade_haClade %in% goodLst)
# value2 <- subset(value, inp$naClade_haClade %in% goodLst)
# group2 <- subset(group, inp$naClade_haClade %in% goodLst)
# data2 = subset(data, inp$naClade_haClade %in% goodLst)
# 
# #goodLst2 also excludes clades with fewer than 20 sequences
# goodLst2 = c("N1.C.A.1_1A.2", "N1.C.A.1_1A.3.3.3", "N1.C.C.3_1A.3.3.3", 
#              "N1.C.C.3_1B.2.1", "N1.C.D.1_1A.3.3.3", "N1.C.D.1_1B.2.2.1", 
#              "N1.C.D.2_1A.2", "N1.C.D.2_1A.3.2", "N1.C.D.2_1A.3.3.3", 
#              "N1.C.D.2_1B.2.1", "N1.C.D.2.1_1A.3.3.3", "N1.C.D.2.1_1B.2.1", 
#              "N1.C.D.2.1_1B.2.2.1", "N1.C.D.2.1_1B.2.2.2", "1.C.D.2.2_1A.3.3.2", 
#              "N1.C.D.2.2_1A.3.3.3", "N1.P_1A.1.1", "N1.P_1A.2-3-like", 
#              "N1.P_1A.3.3.2", "N1.P_1A.3.3.3", "N1.P_1B.2.1", "N1.P_1B.2.2.2")
# time3 <- subset(time, inp$naClade_haClade %in% goodLst2)
# value3 <- subset(value, inp$naClade_haClade %in% goodLst2)
# group3 <- subset(group, inp$naClade_haClade %in% goodLst2)
# data3 = subset(data, inp$naClade_haClade %in% goodLst2)

#goodLst3 also excludes clades with fewer than 30 sequences
goodLst3 = c("N1.C.C.3_1A.3.3.3", "N1.C.C.3_1B.2.1", "N1.C.D.1_1A.3.3.3", 
             "N1.C.D.1_1B.2.2.1", "N1.C.D.2_1A.2", "N1.C.D.2_1A.3.2", 
             "N1.C.D.2_1A.3.3.3", "N1.C.D.2_1B.2.1", "N1.C.D.2.1_1A.3.3.3", 
             "N1.C.D.2.1_1B.2.1", "N1.C.D.2.1_1B.2.2.1", "N1.C.D.2.1_1B.2.2.2", 
             "N1.C.D.2.2_1A.3.3.2", "N1.C.D.2.2_1A.3.3.3", "N1.P_1A.1.1", 
             "N1.P_1A.2-3-like", "N1.P_1A.3.3.2", "N1.P_1A.3.3.3", 
             "N1.P_1B.2.1", "N1.P_1B.2.2.2")
time4 <- subset(time, inp$naClade_haClade %in% goodLst3)
value4 <- subset(value, inp$naClade_haClade %in% goodLst3)
group4 <- subset(group, inp$naClade_haClade %in% goodLst3)
data4 = subset(data, inp$naClade_haClade %in% goodLst3)

#plot data
# plot.new()
# pdf("nahaPairsOTstacked_10yrs_byMonth.pdf", height=5.5, width=12)
# ggplot(data, aes(x=time, y=value, fill=group)) + 
#   geom_area() + labs(x="time", y="NA-HA pair occurances")
# dev.off()
# 
# plot.new()
# pdf("nahaPairsOTstacked_10yrs_byMonth.pdf", height=5.5, width=12)
# ggplot(data2, aes(x=time2, y=value2, fill=group2)) + 
#   geom_area() + labs(x="time", y="NA-HA pair occurances")
# dev.off()
# 
# plot.new()
# pdf("nahaPairsOTstacked_10yrs_byMonth.pdf", height=5.5, width=12)
# ggplot(data3, aes(x=time3, y=value3, fill=group3)) + 
#     geom_area() + labs(x="time", y="NA-HA pair occurances")
# dev.off()

plot.new()
pdf("nahaPairsOTstacked_10yrs_byMonth.pdf", height=5.5, width=12)
ggplot(data4, aes(x=time4, y=value4, fill=group4)) + 
    geom_area() + labs(x="time", y="NA-HA pair occurances", fill="NA-HA pairs") + 
    ggtitle("NA-HA pairs of major NA clades over time") + 
    theme(plot.title=element_text(hjust=0.5)) + 
    scale_x_continuous(breaks=seq(3,129,3), label=as.character(seq(3,129,3)))
dev.off()


#Now do calculations for plotting percentages rather than totals
data5 = inp %>%
    group_by(monthNum, naClade_haClade) %>%
    summarise(n = sum(instance)) %>%
    mutate(percentage = n / sum(n))

#Plot for percentages
plot.new()
pdf("nahaPairsOTstacked_10yrs_byMonthPerc.pdf", height=5.5, width=12)
ggplot(data5, aes(x=monthNum, y=percentage, fill=naClade_haClade)) + 
    geom_area() + labs(x="time", y="NA-HA pair occurances", fill="NA-HA pairs") + 
    ggtitle("NA-HA pairs of major NA clades over time") + 
    theme(plot.title=element_text(hjust=0.5))
dev.off()



