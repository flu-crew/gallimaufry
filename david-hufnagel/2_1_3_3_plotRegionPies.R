#This script is designed to use an input file containing information about
#  all strains in the N1 data set and associated clades and regions and make 
#  plots of all regions present in each clade.  We could ask which clades are 
#  present in each region, but we're asking where is this clade most prominent
#  rather than what is the NA clade composition of each region.
#  Created by David E. Hufnagel on Apr 6, 2021
library(plyr)
library(ggplot2)

setwd("/Users/david.hufnagel/Documents/2_Research/2_2021/1_N1project/3_AyrData/1_cladeSelection")
data_all = read.table("allN1s_v4_regData2.tab")


#subset data
data_N1.H = subset(data_all, data_all$V2=="N1.H")
data_N1.P = subset(data_all, data_all$V2=="N1.P")
data_N1.E.1 = subset(data_all, data_all$V2=="N1.E.1")
data_N1.C = subset(data_all, data_all$V2=="N1.C")
data_N1.C.1 = subset(data_all, data_all$V2=="N1.C.1")
data_N1.C.1.1 = subset(data_all, data_all$V2=="N1.C.1.1")
data_N1.C.1.2 = subset(data_all, data_all$V2=="N1.C.1.2")
data_N1.C.2 = subset(data_all, data_all$V2=="N1.C.2")
data_N1.C.2.1 = subset(data_all, data_all$V2=="N1.C.2.1")
data_N1.C.3 = subset(data_all, data_all$V2=="N1.C.3")
data_N1.C.3.1 = subset(data_all, data_all$V2=="N1.C.3.1")
data_N1.C.3.2 = subset(data_all, data_all$V2=="N1.C.3.2")

#Process file into groups and frequencies
groups_N1.H = count(data_N1.H$V3)$x
freqs_N1.H = count(data_N1.H$V3)$freq

groups_N1.P = count(data_N1.P$V3)$x
freqs_N1.P = count(data_N1.P$V3)$freq

groups_N1.P = count(data_N1.P$V3)$x
freqs_N1.P = count(data_N1.P$V3)$freq

groups_N1.E.1 = count(data_N1.E.1$V3)$x
freqs_N1.E.1 = count(data_N1.E.1$V3)$freq

groups_N1.C = count(data_N1.C$V3)$x
freqs_N1.C = count(data_N1.C$V3)$freq

groups_N1.C.1 = count(data_N1.C.1$V3)$x
freqs_N1.C.1 = count(data_N1.C.1$V3)$freq

groups_N1.C.1.1 = count(data_N1.C.1.1$V3)$x
freqs_N1.C.1.1 = count(data_N1.C.1.1$V3)$freq

groups_N1.C.1.2 = count(data_N1.C.1.2$V3)$x
freqs_N1.C.1.2 = count(data_N1.C.1.2$V3)$freq

groups_N1.C.2 = count(data_N1.C.2$V3)$x
freqs_N1.C.2 = count(data_N1.C.2$V3)$freq

groups_N1.C.2.1 = count(data_N1.C.2.1$V3)$x
freqs_N1.C.2.1 = count(data_N1.C.2.1$V3)$freq

groups_N1.C.3 = count(data_N1.C.3$V3)$x
freqs_N1.C.3 = count(data_N1.C.3$V3)$freq

groups_N1.C.3.1 = count(data_N1.C.3.1$V3)$x
freqs_N1.C.3.1 = count(data_N1.C.3.1$V3)$freq

groups_N1.C.3.2 = count(data_N1.C.3.2$V3)$x
freqs_N1.C.3.2 = count(data_N1.C.3.2$V3)$freq


#plot data by percent
groups = c(rep("N1.H (n=11)", length(groups_N1.H)), rep("N1.P (n=629)", length(groups_N1.P)), 
           rep("N1.E.1 (n=18)", length(groups_N1.E.1)), rep("N1.C (n=171)", length(groups_N1.C)), 
           rep("N1.C.1 (n=125)", length(groups_N1.C.1)), rep("N1.C.1.1 (n=22) ", length(groups_N1.C.1.1)), 
           rep("N1.C.1.2 (n=37) ", length(groups_N1.C.1.2)), rep("N1.C.2 (n=109)", length(groups_N1.C.2)), 
           rep("N1.C.2.1 (n=122) ", length(groups_N1.C.2.1)), rep("N1.C.3 (n=1230)", length(groups_N1.C.3)), 
           rep("N1.C.3.1 (n=711) ", length(groups_N1.C.3.1)), rep("N1.C.3.2 (n=543) ", length(groups_N1.C.3.2)))
regions = c(groups_N1.H, groups_N1.P, groups_N1.E.1, groups_N1.C, groups_N1.C.1, 
            groups_N1.C.1.1, groups_N1.C.1.2, groups_N1.C.2, groups_N1.C.2.1, 
            groups_N1.C.3, groups_N1.C.3.1, groups_N1.C.3.2)
freqs = c(freqs_N1.H, freqs_N1.P, freqs_N1.E.1, freqs_N1.C, 
          freqs_N1.C.1, freqs_N1.C.1.1, freqs_N1.C.1.2, freqs_N1.C.2, 
          freqs_N1.C.2.1, freqs_N1.C.3, freqs_N1.C.3.1, freqs_N1.C.3.2)
toPlot = data.frame(groups,regions,freqs)

plot.new()
pdf("regionBarPlot.pdf")
ggplot(toPlot, aes(fill=regions, y=freqs, x=groups)) +
    geom_bar(position="fill", stat="identity") + 
    theme(axis.text.x = element_text(angle = 90))# +
    #geom_line(data=testAll, aes(x=testX, y=testNs), color="black")
dev.off()


testNs = c(100,22,26,34,50,21,16,700,900,14,120,666)
testX = seq(testNs)
testAll = data.frame(testX, testNs)
plot.new()
pdf("regionBarPlot.pdf")
ggplot(data=testAll, aes(x=testX, y=testNs), color="black") + 
    geom_line()
dev.off()

