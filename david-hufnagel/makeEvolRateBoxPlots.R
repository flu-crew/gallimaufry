#This script is designed to take .log files from BEAST, remove burn-in data,
#  and make boxplots of evolutionary rates comparing all the  clades and 
#  lineages we have for the 1st and 2nd codon position, the 3rd codon position
#  and all nucleotides together
#Created by David E. Hufnagel on Jan 18, 2021

#Libraries
require(ggplot2)


#Load in data
clall = read.csv("N1classical_r1_SRD06_UCLN_GMRF_200M_May21.log", skip = 4, header = T, sep="\t")
n1pall = read.csv("N1P_SRD06_strict_GMRF_200M_Aug2.log", skip = 4, header = T, sep="\t")
n1c2all = read.csv("N1C2_SRD06_strict_GMRF_200M_Nov2.log", skip = 4, header = T, sep="\t")
n1c21all = read.csv("N1C21_SRD06_strict_GMRF_200M_Nov9.log", skip = 4, header = T, sep="\t")
n1c3all = read.csv("N1C3_r1_hkyGamma4_GMRF_200M_May20.log", skip = 4, header = T, sep="\t")
n1c31all = read.csv("N1C31_SRD06_strict_GMRF_200M.log", skip = 4, header = T, sep="\t")
n1c32all = read.csv("N1C32_SRD09_strict_GMRF_200M_May21.log", skip = 4, header = T, sep="\t")


#Burn-in 10% of data (removes the first 1001 rows of data from the log file)
clsub = clall[-c(1:1001),] 
n1psub = n1pall[-c(1:1001),] 
n1c2sub = n1c2all[-c(1:1001),] 
n1c21sub = n1c21all[-c(1:1001),] 
n1c3sub = n1c3all[-c(1:1001),] 
n1c31sub = n1c31all[-c(1:1001),]
n1c32sub = n1c32all[-c(1:1001),] 


#Extract evolutionary rates
clMean = array(unlist(clsub["default.meanRate"]), dim=c(1,9000))
n1PMean = array(unlist(n1psub["meanRate"]), dim=c(1,9000))
n1c2Mean = array(unlist(n1c2sub["meanRate"]), dim=c(1,9000))
n1c21Mean = array(unlist(n1c21sub["meanRate"]), dim=c(1,9000))
n1c3Mean = array(unlist(n1c3sub["meanRate"]), dim=c(1,9000))
n1c31Mean = array(unlist(n1c31sub["meanRate"]), dim=c(1,9000))
n1c32Mean = array(unlist(n1c32sub["meanRate"]), dim=c(1,9000))


cl_12 = array(unlist(clsub["CP1.2.mu"]), dim=c(1,9000))*clMean
n1P_12 = array(unlist(n1psub["CP1.2.mu"]), dim=c(1,9000))*n1PMean
n1c2_12 = array(unlist(n1c2sub["CP1.2.mu"]), dim=c(1,9000))*n1c2Mean
n1c21_12 = array(unlist(n1c21sub["CP1.2.mu"]), dim=c(1,9000))*n1c21Mean
n1c3_12 = array(unlist(n1c3sub["CP1.2.mu"]), dim=c(1,9000))*n1c3Mean
n1c31_12 = array(unlist(n1c31sub["CP1.2.mu"]), dim=c(1,9000))*n1c31Mean
n1c32_12 = array(unlist(n1c32sub["CP1.2.mu"]), dim=c(1,9000))*n1c32Mean


cl_3 = array(unlist(clsub["CP3.mu"]), dim=c(1,9000))*clMean
n1P_3 = array(unlist(n1psub["CP3.mu"]), dim=c(1,9000))*n1PMean
n1c2_3 = array(unlist(n1c2sub["CP3.mu"]), dim=c(1,9000))*n1c2Mean
n1c21_3 = array(unlist(n1c21sub["CP3.mu"]), dim=c(1,9000))*n1c21Mean
n1c3_3 = array(unlist(n1c3sub["CP3.mu"]), dim=c(1,9000))*n1c3Mean
n1c31_3 = array(unlist(n1c31sub["CP3.mu"]), dim=c(1,9000))*n1c31Mean
n1c32_3 = array(unlist(n1c32sub["CP3.mu"]), dim=c(1,9000))*n1c32Mean


#Make grouped boxplots
##Combine the data
codPos = rep(c("General", "1st & 2nd nuc.", "3rd nuc."), each=7*9000) #The prefixes are to ensure a certain order
clade = c(rep(c("C. Lineage", "N1.C.2", "N1.C.2.1", "N1.C.3", "N1.C.3.1", "N1.C.3.2", "N1.P"), each=9000), rep(c("C. Lineage", "N1.C.2", "N1.C.2.1", "N1.C.3", "N1.C.3.1", "N1.C.3.2", "N1.P"), each=9000), rep(c("C. Lineage", "N1.C.2", "N1.C.2.1", "N1.C.3", "N1.C.3.1", "N1.C.3.2", "N1.P"), each=9000))
y = c(clMean, n1c2Mean, n1c21Mean, n1c3Mean, n1c31Mean, n1c32Mean, n1PMean, cl_12, n1c2_12, n1c21_12, n1c3_12, n1c31_12, n1c32_12, n1P_12, cl_3, n1c2_3, n1c21_3, n1c3_3, n1c31_3, n1c32_3, n1P_3)*1000
data = data.frame(codPos, clade, y)


##Plot the data
plot.new()
pdf("evolRatesBoxPlots.pdf", width=7, height=4)
ggplot(data, aes(x=codPos, y=y, fill=clade)) +
  geom_boxplot() + xlab("") + ylab("Molecular Substitution Rate (subs/site/year) * 1000") +
  guides(fill = guide_legend(title = "taxa")) +
  scale_x_discrete(limits=c("General", "1st & 2nd nuc.", "3rd nuc.")) +
  scale_y_continuous(breaks=seq(0,0.011,0.001)*1000)
dev.off()






