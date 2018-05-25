t = read.csv("AllTimes_WolfSheepPredation_16threads.csv")
AllTimes_WolfSheepPredation_NL4Py = t[1:50,]
t = read.csv("AllTimes_WolfSheepPredation_8threads.csv")
AllTimes_WolfSheepPredation_NL4Py = rbind(AllTimes_WolfSheepPredation_NL4Py,t[1:50,])
t = read.csv("AllTimes_WolfSheepPredation_4threads.csv")
AllTimes_WolfSheepPredation_NL4Py = rbind(AllTimes_WolfSheepPredation_NL4Py,t[1:50,])
t = read.csv("AllTimes_WolfSheepPredation_11000.csv")
AllTimes_WolfSheepPredation_NL4Py = rbind(AllTimes_WolfSheepPredation_NL4Py,t[1:50,])
t = read.csv("AllTimes_WolfSheepPredation_1.csv")
AllTimes_WolfSheepPredation_NL4Py = rbind(AllTimes_WolfSheepPredation_NL4Py,t[1:50,])
AllTimes_WolfSheepPredation_NL4Py = AllTimes_WolfSheepPredation_NL4Py[,2:4]

colnames(AllTimes_WolfSheepPredation_NL4Py) = c("Runs","Threads","Time.ms")
library(ggplot2)
ggplot(AllTimes_WolfSheepPredation_NL4Py, aes(x=as.factor(Runs), y=Time.ms, fill = as.factor(Threads))) + geom_boxplot()

AllTimes_WolfSheepPredation_NL4Py = subset(AllTimes_WolfSheepPredation_NL4Py, Runs > 11000)
AllTimes_WolfSheepPredation_NL4Py$Time.ms = AllTimes_WolfSheepPredation_NL4Py$Time.ms / 1000
colnames(AllTimes_WolfSheepPredation_NL4Py) = c("Runs","Threads","Time.s")
library(Rmisc)
AllTimes_WolfSheepPredation_NL4Py_plot = summarySEwithin(AllTimes_WolfSheepPredation_NL4Py, measurevar="Time.s", withinvars=c("Threads","Runs"))


ggplot(AllTimes_WolfSheepPredation_NL4Py_plot, aes(x=as.factor(Runs), y=Time.s, fill = as.factor(Threads))) + geom_bar(position=position_dodge(), stat="identity") + geom_errorbar(position=position_dodge(.9), width=.25, aes(ymin=Time.s-ci, ymax=Time.s+ci))+ theme(text = element_text(size=16)) + scale_fill_discrete(name = "Threads") + ylab("Time Taken in Seconds") + xlab("Model Runs Performed")+
  scale_y_continuous(breaks = pretty(AllTimes_WolfSheepPredation_NL4Py_plot$Time.s, n = 10))


####################################

ScheduledReportersRepeatReporterComparison = read.csv("ScheduledReportersRepeatReporterComparison.csv")
ScheduledReportersRepeatReporterComparison$connector = ifelse(ScheduledReportersRepeatReporterComparison$connector =="NL4Py","NL4Py","PyNetLogo with IPCluster")
ScheduledReportersRepeatReporterComparison$time.s = ScheduledReportersRepeatReporterComparison$time.ms/1000
ggplot(ScheduledReportersRepeatReporterComparison, aes(connector,time.s,group=connector)) + geom_boxplot(outlier.shape = NA,width=0.5) + theme(text = element_text(size = 16), panel.background = element_rect(fill = "white"), panel.grid.major = element_line(colour = "grey"), panel.grid.minor = element_line(colour = "grey"), panel.grid.major.x = element_blank()) + ylim(350,550) + ylab("Execution Time in Seconds") + xlab("Python to NetLogo Connector")

####################################

ReportersComparison = read.csv("Times_Comparison_Reporters.csv")
ReportersComparison$time.s = ReportersComparison$time.ms/1000
ggplot(ReportersComparison, aes(connector, time.s, group= connector))+  geom_boxplot(outlier.shape = NA,width=0.5) + facet_wrap(~model, scales = "free") + theme(text = element_text(size = 16), panel.background = element_rect(fill = "white"), panel.grid.major = element_line(colour = "grey"), panel.grid.minor = element_line(colour = "grey"), panel.grid.major.x = element_blank())+ ylab("Execution Time in Seconds") + xlab("Python to NetLogo Connector")

####################################

ReportersThreadsComparison = read.csv("Times_Comparison_Threads.csv")
ReportersThreadsComparison$time.s = ReportersThreadsComparison$time.ms/1000
ggplot(subset(ReportersThreadsComparison), aes(runs, time.s, group= runs)) + geom_boxplot() + facet_wrap(~threads)

+ theme(text = element_text(size = 16), panel.background = element_rect(fill = "white"), panel.grid.major = element_line(colour = "grey"), panel.grid.minor = element_line(colour = "grey"), panel.grid.major.x = element_blank())+ ylab("Execution Time in Seconds") + xlab("Python to NetLogo Connector")
