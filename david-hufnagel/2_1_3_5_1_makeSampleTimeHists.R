#This script is designed to take a metadata file of N1 sequences and create
#  Histograms of each circulating clade, all circulating clades, and all clades
#Created by David E. Hufnagel on May 17th, 2021
library(ggplot2)

setwd("/Users/david.hufnagel/Documents/2_Research/2_2021/1_N1project/3_AyrData/5_SpatioTemporalAnalysis/1_samplesOverTimeHists")

#import and sort data by clade
data_all = read.table("strainMetaData_v2_dateMod.txt", header=TRUE, sep="\t")
data_N1P = subset(data_all, data_all$NA_clade=="N1.P")
data_N1C11 = subset(data_all, data_all$NA_clade=="N1.C.1.1")
data_N1C2 = subset(data_all, data_all$NA_clade=="N1.C.2")
data_N1C21 = subset(data_all, data_all$NA_clade=="N1.C.2.1")
data_N1C3 = subset(data_all, data_all$NA_clade=="N1.C.3")
data_N1C31 = subset(data_all, data_all$NA_clade=="N1.C.3.1")
data_N1C32 = subset(data_all, data_all$NA_clade=="N1.C.3.2")
data_circ = subset(data_all, data_all$NA_clade %in% 
                       c("N1.P","N1.C.1.1", "N1.C.2", "N1.C.2.1", "N1.C.3", 
                         "N1.C.3.1", "N1.C.3.2"))  #all circulating clades


#Extract dates from data
dates_all = as.Date(data_all$collection_date, format = c("%m/%d/%Y"))
dates_N1P = as.Date(data_N1P$collection_date, format = c("%m/%d/%Y"))
dates_N1C11 = as.Date(data_N1C11$collection_date, format = c("%m/%d/%Y"))
dates_N1C2 = as.Date(data_N1C2$collection_date, format = c("%m/%d/%Y"))
dates_N1C21 = as.Date(data_N1C21$collection_date, format = c("%m/%d/%Y"))
dates_N1C3 = as.Date(data_N1C3$collection_date, format = c("%m/%d/%Y"))
dates_N1C31 = as.Date(data_N1C31$collection_date, format = c("%m/%d/%Y"))
dates_N1C32= as.Date(data_N1C32$collection_date, format = c("%m/%d/%Y"))
dates_circ= as.Date(data_circ$collection_date, format = c("%m/%d/%Y"))


#plot data.  the number of breaks was determined as the most recent year minus the earliest year in the working data set + 1 to make 1 group per year
plot.new()
pdf("all_dates.pdf")
#hist(dates_all, breaks=90+1)
qplot(dates_all, geom="histogram", bins=90+1, main="all data")
dev.off()

plot.new()
pdf("N1.P_dates.pdf")
#hist(dates_N1P, breaks=11+1)
qplot(dates_N1P, geom="histogram", bins=11+1, main="N1.P")
dev.off()

plot.new()
pdf("N1.C.1.1_dates.pdf")
#hist(dates_N1C11, breaks=20+1)
qplot(dates_N1C11, geom="histogram", bins=20+1, main="N1.C.1.1")
dev.off()

plot.new()
pdf("N1.C.2_dates.pdf")
#hist(dates_N1C2, breaks=16+1)
qplot(dates_N1C2, geom="histogram", bins=16+1, main="N1.C.2")
dev.off()

plot.new()
pdf("N1.C.2.1_dates.pdf")
#hist(dates_N1C21, breaks=13+1)
qplot(dates_N1C21, geom="histogram", bins=13+1, main="N1.C.2.1")
dev.off()

plot.new()
pdf("N1.C.3_dates.pdf")
#hist(dates_N1C3, breaks=17+1)
qplot(dates_N1C3, geom="histogram", bins=17+1, main="N1.C.3")
dev.off()

plot.new()
pdf("N1.C.3.1_dates.pdf")
#hist(dates_N1C31, breaks=8+1)
qplot(dates_N1C31, geom="histogram", bins=8+1, main="N1.C.3.1")
dev.off()

plot.new()
pdf("N1.C.3.2_dates.pdf")
#hist(dates_N1C32, breaks=7+1)
qplot(dates_N1C32, geom="histogram", bins=7+1, main="N1.C.3.2")
dev.off()

plot.new()
pdf("circulatingClade_dates.pdf")
#hist(dates_N1C32, breaks=7+1)
qplot(dates_circ, geom="histogram", bins=7+1, main="circulating clades")
dev.off()

