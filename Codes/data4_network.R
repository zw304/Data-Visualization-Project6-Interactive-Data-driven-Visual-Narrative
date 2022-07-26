library(arules)
library(arulesViz)
library(plotly)
library(ggplot2)
library(tidyverse)
library(visNetwork)
library(igraph)

#BASIC DATA CLEANING
data <- read.csv("GVP_Volcano_List_Holocene.csv", header = T, sep = ',')
str(data)
head(data)

data <- data[,c(8,12,13,14)]
data <- na.omit(data)
head(data)

write.table(data,'trans.txt',sep =",",col.names = F,row.names = F)
#Here I got my transaction data



######ARM
trans <- read.transactions(
  "trans.txt", 
  format = "basket",      #basket or single
  header = FALSE,         
  sep = ",", 
  rm.duplicates = T,  #rm duplicates from transactions
  cols = NULL,            
)
#inspect(trans)


#Min Support 0.2, confidence as 0.6.
rules <- apriori(
  trans, 
  parameter = list(
    target= "rules",
    support=0.2, conf=0.6)
)


inspect(rules[1:10])
## Sort by Sup
SortedRules_sup <- sort(rules, by="support", decreasing=TRUE)
inspect(SortedRules_sup[1:10])

##  SOrt by Conf
SortedRules_conf <- sort(rules, by="confidence", decreasing=TRUE)
inspect(SortedRules_conf[1:10])

## Sort by Lift
SortedRules_lift <- sort(rules, by="lift", decreasing=TRUE)
inspect(SortedRules_lift[1:10])



##Plotly
p1 <- plot(SortedRules_sup[1:10],method="graph",engine='htmlwidget', shading="confidence")
htmlwidgets::saveWidget(as_widget(p1), "network-Sup_TOP10.html")

p2 <- plot(SortedRules_conf[1:10],method="graph",engine='htmlwidget',shading="confidence") 
htmlwidgets::saveWidget(as_widget(p2), "network-conf_TOP10.html")

p3 <- plot(SortedRules_lift[1:10],method="graph",engine='htmlwidget',shading="confidence") 
htmlwidgets::saveWidget(as_widget(p3), "network-Lift_TOP10.html")

