setwd("/Users/david.hufnagel/Documents/2_Research/1_2020/5_N1SelectionReborn/7_HApairing/2_10yrDataOverTime")

#import data
inp = read.table("pairData_10yr_Rinp.txt", sep="\t")

#split up data by NA clade and make a plot for each NA clade
inpSplit = split(inp, inp$V1)
for (naData in inpSplit){
  plotName = sprintf("pairingO10yrs_%s.pdf", naData$V1[1])
  plot.new()
  pdf(plotName)
  
  #split up data by HA clade and make a line for each HA clade
  naDataSplit = split(naData, naData$V2)
  cnt = 0; colors = c(); has = c(); ltys = c()
  for (haData in naDataSplit){
    if (cnt == 0){
      X = haData$V5; Y = haData$V6
      plot(X[!is.na(Y)], Y[!is.na(Y)], type="l", xlim=c(0,130), ylim=c(0, 1), lwd=2, pch=16, bty="n", xaxt="n", yaxt="n", cex.lab=1.2, xlab="time (months since Jan 2010)", ylab="% HA pairing")
      axis(side = 1, lwd = 2, font=2); axis(side = 2, lwd = 2, font=2)
    }
    else
      X = haData$V5; Y = haData$V6
      lines(X[!is.na(Y)], Y[!is.na(Y)], lwd=2, col=cnt+1, lty=cnt+1)
      colors = c(colors, cnt+1); has = c(has, haData$V2[cnt+1]); ltys=c(ltys, cnt+1)
      
    cnt = cnt + 1
  }
  titleName = sprintf("NA-HA pairing over time for %s", naData$V1[1])
  title(main=titleName)
  legend("right", legend=has, pch=15, col=colors, lwd=1, lty=ltys)
  
  box(lwd=2)
  
  dev.off()
}





