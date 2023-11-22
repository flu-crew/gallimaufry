#Based on Michael Zeller's script from Zeller et al. 2021. in Virus Evolution.
#The Purpose of this script is to use BayesTwin to assess the potential 
#statistical significance of differences in evolutionary rates between these
#specific BEAST runs: N1 lineage vs N1.P, N1.P vs N1.C.2, N1.P vs N1.C.2.1,
#N1.P vs N1.C.3, N1.P vs N1.C.3.1, N1.P vs N1.C.3.2, N1.C.2.1 vs N1.C.2,
#N1.C.3.1 vs N1.C.3, and N1.C.3.2 vs N1.C.3



#Libraries
require(ggplot2)
library(BayesTwin)
library(cowplot)



#Functions
plotHistogram <- function(df, x, y) {
  #Calculate
  hiNum <- round(colSums((x-y) > 0)/nrow(x-y),2) #percent of data points where new - old is positive
  loNum <- round(colSums((x-y) < 0)/nrow(x-y),2) #percent of data points where new - old is negative
  
  textPercent <- paste(loNum, "% < 0 < ", hiNum, "%", sep="")
  textXAxis <- expression(paste(mu,"Rate1 - ",mu,"Rate2", sep=""))
  df["muDiff"] = x - y
  hpdLimits <- HPD(x-y)
  
  #Plot
  ggplot(df, aes(x=muDiff)) + 
    geom_histogram(bins=50, colour="black", fill="white", alpha=0.6) +                        # Histrogram
    geom_vline(aes(xintercept=mean(x=muDiff)), color="red", linetype="dashed", size=1) +      # Mean lines
    geom_vline(aes(xintercept=0), color="black", linetype="solid", size=2) +                  # Zero line
    geom_vline(aes(xintercept=hpdLimits[1]), color="blue", linetype="dashed", size=1) +       # Low HPD
    geom_vline(aes(xintercept=hpdLimits[2]), color="blue", linetype="dashed", size=1) +       # High HPD
    annotate(geom="text", x=mean(x-y), y=Inf, label=textPercent, color="red", fontface="bold", vjust=1, hjust=0.5) +
    annotate(geom="text", x=hpdLimits[1], y=0, label=hpdLimits[1], color="blue", fontface="bold", vjust=0, hjust=0) +
    annotate(geom="text", x=hpdLimits[2], y=0, label=hpdLimits[2], color="blue", fontface="bold", vjust=0, hjust=1) +
    scale_x_continuous(name =textXAxis)
}



#Load in data
clall = read.csv("N1classical_r1_SRD06_UCLN_GMRF_200M_May21.log", skip = 4, header = T, sep="\t")
n1pall = read.csv("N1P_SRD06_strict_GMRF_200M_Aug2.log", skip = 4, header = T, sep="\t")
n1c2all = read.csv("N1C2_SRD06_strict_GMRF_200M_Nov2.log", skip = 4, header = T, sep="\t")
n1c21all = read.csv("N1C21_SRD06_strict_GMRF_200M_Nov9.log", skip = 4, header = T, sep="\t")
n1c3all = read.csv("N1C3_r1_hkyGamma4_GMRF_200M_May20.log", skip = 4, header = T, sep="\t")
n1c31all = read.csv("N1C31_SRD06_strict_GMRF_200M.log", skip = 4, header = T, sep="\t")
n1c32all = read.csv("N1C32_SRD09_strict_GMRF_200M_May21.log", skip = 4, header = T, sep="\t")


#Burn-in 10% of data (removes the first 101 rows of data from the log file)
clsub = clall[-c(1:101),] 
n1psub = n1pall[-c(1:101),] 
n1c2sub = n1c2all[-c(1:101),] 
n1c21sub = n1c21all[-c(1:101),] 
n1c3sub = n1c3all[-c(1:101),] 
n1c31sub = n1c31all[-c(1:101),]
n1c32sub = n1c32all[-c(1:101),] 


#Make individual plots
#CL vs N1.P
clsub["n1p.meanRate"] = n1psub["meanRate"] #add N1.P data to CL data so it can serve as the "together" data set
cl_rates = as.matrix(clsub["default.meanRate"])
n1p_rates = as.matrix(n1psub["meanRate"])
(clVn1p_plot = plotHistogram(clsub,cl_rates,n1p_rates))

#N1.P vs N1.C.2
n1psub["n1c2.meanRate"] = n1c2sub["meanRate"]
n1c2_rates = as.matrix(n1c2sub["meanRate"])
(n1pVn1c2_plot = plotHistogram(n1psub,n1p_rates,n1c2_rates))

#N1.P vs N1.C.2.1
n1psub["n1c21.meanRate"] = n1c21sub["meanRate"]
n1c21_rates = as.matrix(n1c21sub["meanRate"])
(n1pVn1c21_plot = plotHistogram(n1psub,n1p_rates,n1c21_rates))

#N1.P vs N1.C.3
n1psub["n1c3.meanRate"] = n1c3sub["meanRate"]
n1c3_rates = as.matrix(n1c3sub["meanRate"])
(n1pVn1c3_plot = plotHistogram(n1psub,n1p_rates,n1c3_rates))

#N1.P vs N1.C.3.1
n1psub["n1c31.meanRate"] = n1c31sub["meanRate"]
n1c31_rates = as.matrix(n1c31sub["meanRate"])
(n1pVn1c31_plot = plotHistogram(n1psub,n1p_rates,n1c31_rates))

#N1.P vs N1.C.3.2
n1psub["n1c32.meanRate"] = n1c32sub["meanRate"]
n1c32_rates = as.matrix(n1c32sub["meanRate"])
(n1pVn1c32_plot = plotHistogram(n1psub,n1p_rates,n1c32_rates))

#N1.C.2.1 vs N1.C.2
n1c2sub["n1c21.meanRate"] = n1c21sub["meanRate"]
(n1c2Vn1c21_plot = plotHistogram(n1c2sub,n1c2_rates,n1c21_rates))

#N1.C.3.1 vs N1.C.3
n1c3sub["n1c31.meanRate"] = n1c31sub["meanRate"]
(n1c31Vn1c3_plot = plotHistogram(n1c3sub,n1c31_rates,n1c3_rates))

#N1.C.3.2 vs N1.C.3
n1c3sub["n1c32.meanRate"] = n1c32sub["meanRate"]
(n1c32Vn1c3_plot = plotHistogram(n1c3sub,n1c32_rates,n1c3_rates))


#Combine the plots into larger Figures
plot.new()
tiff('evolRateStatSig.tiff', units="in", width=13.5, height=9, res=250, compression = 'lzw')

plot_grid(clVn1p_plot, n1pVn1c2_plot, n1pVn1c21_plot,n1pVn1c3_plot, 
          n1pVn1c31_plot, n1pVn1c32_plot, n1c2Vn1c21_plot, n1c31Vn1c3_plot, 
          n1c32Vn1c3_plot,
          # labels = c("CLXX vs N1.P", "N1.P vs N1.C.2", "N1.P vs N1.C.2.1", 
          #            "N1.P vs N1.C.3", "N1.P vs N1.C.3.1", "N1.P vs N1.C.3.2", 
          #            "N1.C.2 vs N1.C.2.1", "N1.C.3.1 vs N1.C.3", "N1.C.3.2 vs N1.C.3"),
          labels = c("A", "B", "C", "D", "E", "F", "G", "H", "I"),
          ncol = 3, nrow = 3)#, label_y=-1)#vjust=c(50,5,5,5,5,5,5,5,5))
dev.off()






























