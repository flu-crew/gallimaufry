#This script is designed to use an input file containing information about
#  all strains in the gamma data set and associated clades and regions and make 
#  plots of all regions present in each clade.  We could ask which clades are 
#  present in each region, but we're asking where is this clade most prominent
#  rather than what is the NA clade composition of each region.
#  Created by David E. Hufnagel on Aug 21, 2023
library(plyr)
library(ggplot2)

setwd("/Users/david.hufnagel/Documents/1_Research/4_2023/5_Gamma/3_regionPlotCEIRR")
data_all = read.table("gammaSeqs_v3_nameFix_regData_cond.tab")


#subset data
data_base= subset(data_all, data_all$V2=="1A.3.3.3")
data_c1 = subset(data_all, data_all$V2=="1A.3.3.3-c1")
data_c2 = subset(data_all, data_all$V2=="1A.3.3.3-c2")
data_c3 = subset(data_all, data_all$V2=="1A.3.3.3-c3")


#Process file into groups and frequencies
groups_base = count(data_base$V3)$x
freqs_base = count(data_base$V3)$freq

groups_c1 = count(data_c1$V3)$x
freqs_c1 = count(data_c1$V3)$freq

groups_c2 = count(data_c2$V3)$x
freqs_c2 = count(data_c2$V3)$freq

groups_c3 = count(data_c3$V3)$x
freqs_c3 = count(data_c3$V3)$freq

groups_all = count(data_all$V3)$x
freqs_all = count(data_all$V3)$freq


#plot data by percent
groups = c(rep("All data", length(groups_all)), rep("1A.3.3.3 (n=134)", 
          length(groups_base)), rep("1A.3.3.3-c1 (n=168)", length(groups_c1)), 
          rep("1A.3.3.3-c2 (n=361)", length(groups_c2)), 
          rep("1A.3.3.3-c3 (n=3066)", length(groups_c3)))
regions = c(groups_all, groups_base, groups_c1, groups_c2, groups_c3)
freqs = c(freqs_all, freqs_base, freqs_c1, freqs_c2, freqs_c3)
toPlot = data.frame(groups,regions,freqs)

plot.new()
pdf("gammaRegionBarPlot.pdf", width = 8, height =6)
ggplot(toPlot, aes(fill=regions, y=freqs, x=groups)) +
    geom_bar(position="fill", stat="identity") + 
    theme(axis.text.x = element_text(angle = 90, size = 14, color="black"), 
          axis.title.y =element_text(angle = 90, size = 16),
          legend.title=element_text(size=16), legend.text = element_text(size=14)) + #, legend.position = c(1,0.4)) +
    xlab("") + ylab("proportion")
dev.off()

