#This script is designed to take data files originally from Satscan and
#  processed in Python and plot their data with time on the X-axis and clades
#  on the Y-axis with RR represented by colors. It's essentially a high-tech
#  timeline
#  Created by David E. Hufnagel on April 5, 2022
#Updated by David E. Hufnagel on April 13, 2022 to use the new joint (clade and 
#  clade pair) SG values and create the legend that includes all new joint SG 
#  values

library(ggplot2)
library(vistime)
library(scales)


setwd("/Users/david.hufnagel/Documents/1_Research/3_2022/2_N1diversity/2_makingSatscanPlots")
satData = read.table("statsPoissResults_pairs_rr2.txt", header = TRUE, 
                     row.names = "uniqueID", sep = "\t", comment.char = "%")



#Organize data
satData$startDate = as.Date(satData$startDate)
satData$endDate = as.Date(satData$endDate)
plotFrame = data.frame(Position = satData$clusterID, 
                       Name = satData$cladePair, start = satData$startDate, 
                       end = satData$endDate, color = satData$Rcolor, 
                       rr = satData$RR, cas = satData$numCases)

#Plot data
plot.new()
pdf("satscanPoissonPairs2.pdf", height=5, width=7.9)
gg_vistime(plotFrame, col.event = "Position", col.group = "Name", title = "") + 
  ggplot2::theme(axis.text = element_text(size=11), axis.text.x = element_text(angle=90, vjust=0.6)) +
  scale_x_datetime(breaks = breaks_width("1 year"), labels = date_format("%Y"))
dev.off()
  

plot.new()
pdf("satscanPoissonPairs_colorLegend.pdf", height=5, width=3)
#make a fake plot using the same data and add a legend to it (the legend for colors)
plot(plotFrame$rr ~ plotFrame$cas, col=plotFrame$color)
legend(list(x=170, y=200), c("4-8","8-15","15-21","21-inf"), title="RR:",
       col=c("#FEF001", "#FFB403", "#fd6601", "red"), 
       pch=c(15,15,15,15,15,15), box.lwd=1.2, lty=0, cex=1.0, pt.cex=2.5, y.intersp=1.5)
dev.off()


plot.new()
pdf("satscanPoissonPairs_clusterLegend2.pdf", height=8, width=6)
#make a fake plot using the same data and add a legend to it (the legend for state cluster names)
plot(plotFrame$rr ~ plotFrame$cas, col=plotFrame$color)
legend(list(x=120, y=250), c(" SG01 = AL,AR,IL,LA,MO,MS,", "             OK,TN", "SG02 = NE,SD", 
                             " SG03 = AL,AR,DC,DE,GA,IL,", "              IN,KY,MD,MI,MO,MS,", 
                             "              NC,OH,PA,SC,TN,VA,", "              WI,WV", "SG04 = NC,VA", 
                             "SG05 = IA,IL,WI", " SG06 = AK,AZ,CA,CO,HI,ID,", 
                             "              KS,MN,MT,ND,NE,NM,", "              NV,OK,OR,SD,TX,UT,", "             WA,WY", 
                             " SG07 = IL,IN,KY,NC,OH,SC,", "             TN,VA,WV", "SG08 = MN,ND,SD", 
                             " SG09 = AL,AR,AZ,CO,KS,LA,", "              MO,MS,NE,NM,OK,TX", 
                             "SG10 = IN,KY,OH", " SG11 = AR,AZ,CA,CO,ID,KS,", 
                             "              MO,MT,NC,ND,NE,NM,", "               NV,OK,OR,TX,UT,WA,WY", 
                             "SG12 = IL,MI,WI", " SG13 = CT,DC,DE,IL,IN,KY,", 
                             "              MA,MD,ME,MI,NC,NH,", "              NJ,NY,OH,PA,RI,SC,", 
                             "              VA,VT,WI,WV", " SG14 = KS,MN,ND,NE,SD", 
                             " SG15 = AZ,CO,NM,OK,TX,UT", " SG16 = AR,LA,MO,MS,TN", 
                             " SG17 = AZ,CA,CO,ID,KS,MT,", "               NC,NE,NM,NV,OK,OR,", 
                             "              TX,UT,WY", "SG18 = IL,IN,OH", 
                             " SG19 = AZ,CA,CO,ID,KS,MN,", "               MT,ND,NE,NM,NV,OR,", 
                             "              SD,UT,WA,WY", "SG20 = MN,ND", 
                             " SG21 = AK,CA,ID,MN,MT,ND,", "              NV,OR,SD,UT,WA,WY"),
       pch="", box.lwd=1.2, lty=0, cex=0.7, pt.cex=0.0, y.intersp=0.9, adj=0.04)
dev.off()




