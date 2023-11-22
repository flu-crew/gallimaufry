#This script is designed to use an input file containing information about
#  all strains in the N1 data set and associated clades and regions and make 
#  plots of all regions present in each clade.  We could ask which clades are 
#  present in each region, but we're asking where is this clade most prominent
#  rather than what is the NA clade composition of each region.
#  Created by David E. Hufnagel on Apr 6, 2021
#  All data was added as a comparison on May 20, 2021
#  This version was created for plotting all data including global data in
#  termms of countries over clades
library(plyr)
library(ggplot2)

setwd("/Users/david.hufnagel/Documents/1_Research/4_2023/2_N1diversity/1_WorldwideN1Phylogeny/3_plotContinentHist")
data_all = read.csv("combinedN1s_cladeFill_contData.csv")


#subset data
data_N1.H = subset(data_all, data_all$clade=="N1.H")
data_N1.P = subset(data_all, data_all$clade=="N1.P")
data_N1.E = subset(data_all, data_all$clade=="N1.E")
data_N1.E.1 = subset(data_all, data_all$clade=="N1.E.1")
data_N1.C = subset(data_all, data_all$clade=="N1.C")
data_N1.C.1 = subset(data_all, data_all$clade=="N1.C.1")
data_N1.C.1.1 = subset(data_all, data_all$clade=="N1.C.1.1")
data_N1.C.1.2 = subset(data_all, data_all$clade=="N1.C.1.2")
data_N1.C.2 = subset(data_all, data_all$clade=="N1.C.2")
data_N1.C.2.1 = subset(data_all, data_all$clade=="N1.C.2.1")
data_N1.C.3 = subset(data_all, data_all$clade=="N1.C.3")
data_N1.C.3.1 = subset(data_all, data_all$clade=="N1.C.3.1")
data_N1.C.3.2 = subset(data_all, data_all$clade=="N1.C.3.2")

#Process file into groups and frequencies
groups_N1.H = count(data_N1.H$continent)$x
freqs_N1.H = count(data_N1.H$continent)$freq

groups_N1.P = count(data_N1.P$continent)$x
freqs_N1.P = count(data_N1.P$continent)$freq

groups_N1.P = count(data_N1.P$continent)$x
freqs_N1.P = count(data_N1.P$continent)$freq

groups_N1.E = count(data_N1.E$continent)$x
freqs_N1.E = count(data_N1.E$continent)$freq

groups_N1.E.1 = count(data_N1.E.1$continent)$x
freqs_N1.E.1 = count(data_N1.E.1$continent)$freq

groups_N1.C = count(data_N1.C$continent)$x
freqs_N1.C = count(data_N1.C$continent)$freq

groups_N1.C.1 = count(data_N1.C.1$continent)$x
freqs_N1.C.1 = count(data_N1.C.1$continent)$freq

groups_N1.C.1.1 = count(data_N1.C.1.1$continent)$x
freqs_N1.C.1.1 = count(data_N1.C.1.1$continent)$freq

groups_N1.C.1.2 = count(data_N1.C.1.2$continent)$x
freqs_N1.C.1.2 = count(data_N1.C.1.2$continent)$freq

groups_N1.C.2 = count(data_N1.C.2$continent)$x
freqs_N1.C.2 = count(data_N1.C.2$continent)$freq

groups_N1.C.2.1 = count(data_N1.C.2.1$continent)$x
freqs_N1.C.2.1 = count(data_N1.C.2.1$continent)$freq

groups_N1.C.3 = count(data_N1.C.3$continent)$x
freqs_N1.C.3 = count(data_N1.C.3$continent)$freq

groups_N1.C.3.1 = count(data_N1.C.3.1$continent)$x
freqs_N1.C.3.1 = count(data_N1.C.3.1$continent)$freq

groups_N1.C.3.2 = count(data_N1.C.3.2$continent)$x
freqs_N1.C.3.2 = count(data_N1.C.3.2$continent)$freq

groups_all = count(data_all$continent)$x
freqs_all = count(data_all$continent)$freq



#plot data by percent
groups = c(rep("All data", length(groups_all)), rep("N1.H (n=23)", length(groups_N1.H)), rep("N1.P (n=1247)", length(groups_N1.P)), 
           rep("N1.E (n=1389)", length(groups_N1.E)), rep("N1.E.1 (n=18)", length(groups_N1.E.1)), rep("N1.C (n=264)", length(groups_N1.C)), 
           rep("N1.C.1 (n=422)", length(groups_N1.C.1)), rep("N1.C.1.1 (n=22) ", length(groups_N1.C.1.1)), 
           rep("N1.C.1.2 (n=37) ", length(groups_N1.C.1.2)), rep("N1.C.2 (n=111)", length(groups_N1.C.2)), 
           rep("N1.C.2.1 (n=122) ", length(groups_N1.C.2.1)), rep("N1.C.3 (n=1232)", length(groups_N1.C.3)), 
           rep("N1.C.3.1 (n=711) ", length(groups_N1.C.3.1)), rep("N1.C.3.2 (n=543) ", length(groups_N1.C.3.2)))
regions = c(groups_all, groups_N1.H, groups_N1.P, groups_N1.E, groups_N1.E.1, groups_N1.C, groups_N1.C.1, 
            groups_N1.C.1.1, groups_N1.C.1.2, groups_N1.C.2, groups_N1.C.2.1, 
            groups_N1.C.3, groups_N1.C.3.1, groups_N1.C.3.2)
freqs = c(freqs_all, freqs_N1.H, freqs_N1.P, freqs_N1.E, freqs_N1.E.1, freqs_N1.C, 
          freqs_N1.C.1, freqs_N1.C.1.1, freqs_N1.C.1.2, freqs_N1.C.2, 
          freqs_N1.C.2.1, freqs_N1.C.3, freqs_N1.C.3.1, freqs_N1.C.3.2)
toPlot = data.frame(groups, regions, freqs)

plot.new()
pdf("continentBarPlot.pdf")
ggplot(toPlot, aes(fill=regions, y=freqs, x=groups)) +
    geom_bar(position="fill", stat="identity") + 
    theme(axis.text.x = element_text(angle = 90)) +
    labs(x = "NA clades", y = "Continent Frequency") +
    ggtitle("The Distribution of Continents Within global N1 NA Clades") + 
    theme(plot.title = element_text(hjust = 0.5)) +
    guides(fill=guide_legend(title="Continents"))
dev.off()

