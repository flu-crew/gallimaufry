#This script is designed to plot a linear regression of IAV cases in swine over
#pig populations with each state as a data point.
#Created by David E. Hufnagel on March 30, 2022
setwd("/Users/david.hufnagel/Documents/1_Research/3_2022/2_N1diversity/1_IAVvsSwinePop")


###  define functions  ###
#This function extracts the p-value from an lm summary object.  It is taken from http://stackoverflow.com/questions/5587676/pull-out-p-values-and-r-squared-from-a-linear-regression
GetPval = function (modelobject) {
  if (class(modelobject) != "lm") stop("Not an object of class 'lm' ")
  f <- summary(modelobject)$fstatistic
  p <- pf(f[1],f[2],f[3],lower.tail=F)
  attributes(p) <- NULL
  return(p)
}


#This function creates a y=mx+b style formula from an lm summary object. 
#my version
GetForm = function (model) {
  sprintf("y = %.4f * %s + %.4f", coefficients(model)[-1], 
          names(coefficients(model)[-1]), coefficients(model)[1]) 
}



#gather data
data = read.csv("SwineReportsVsPopulation.csv", header=TRUE)
pigs = data$Average.swine.population
cases = data$Cases
fit = lm(cases ~ pigs, data = data)


#plot
pdf("CasesOverPigs.pdf", height=6, width=9)
plot(pigs, cases, ylab="", xlab="", main="",lwd=1.3)                               #plot data points
mtext("swine population per state", side=1, cex=1.25, line=2.65)                   #plot x-axis
mtext("IAV cases in swine per state", side=2, cex=1.25, line=2.65)                 #plot y-axis
title("IAV cases over swine population per U.S. state", cex.main=1.35)             #plot title
abline(fit, col="blue", lwd=1.3)                                                   #plot fine line
p = GetPval(fit); text(x=15600,y=960, labels=sprintf("p-value: %.4e",p), cex=1.05) #fit line p-val
form = GetForm(fit); text(x=13700,y=1030, labels=form, cex=1.05)                   #fit line formula
r2 = summary(fit)$r.squared; text(x=19000,y=1030, 
                                  labels=sprintf("R^2: %.4f",r2), cex=1.05)        #fit line R^2
text("MI", x=11253, y=55); text("IL", x=4892, y=428)                               #label "outliers"
text("IN", x=3450, y=252); text("MN", x=8221, y=505)                               #label "outliers" 
text("IA", x=21600, y=1000)                                                        #label "outliers"
dev.off()
