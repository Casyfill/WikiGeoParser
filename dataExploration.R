setwd('/Users/casy/Dropbox/My_Projects/Karmatskiy_City/WikiGeoParser/data/')

df <- read.csv('result_stats.csv')
names(df)

library(ggplot2)

ggplot(df, aes(x=seen, y=lnum)) + geom_point()



innerSeen <- df[df$seen<2000,]
innerSeen2 <- df[df$seen<200,]
ggplot(innerSeen2, aes(x=seen)) + geom_histogram(fill='grey', col='black')

# cluster seens into ranks
rankdefine <- function(x){
  r<-1
  for(i in c(100,500,2000,7000)) if(x>i) r<-i
  as.cr
}


df$myRank <- sapply(df$seen, rankdefine)

df[df$myRank==100,]$myRank <- 2
df[df$myRank==500,]$myRank <- 3
df[df$myRank==2000,]$myRank <- 4
df[df$myRank==7000,]$myRank <- 5


summary(as.factor(df$myRank))

write.csv(df,'seen_ranked.csv')
