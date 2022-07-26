
###leaflet: 
library(tidyverse)
#install.packages("sf")
library(sf)
#install.packages("mapview")
library(mapview)
library(htmlwidgets)
library(leaflet)


vol<- read.csv("data1_GVP_Volcano_List_Holocene.csv")

head(vol) 
str(vol)

###
map2 <- leaflet() %>%
  addTiles() %>%
  addMarkers(data=vol, 
             clusterOptions = markerClusterOptions(),
             clusterId = "quakesCluster",
             popup=vol$Region)%>% 
  addProviderTiles(providers$Esri.WorldImagery)
map2
mapshot(map2, url = paste0(getwd(), "/figure1.html"))
##


# draw another map --> too messy --> choose the first plot
leaflet() %>% 
  # add first tile
  addTiles(group="One") %>%
  # add second tile
  addProviderTiles(providers$Esri.WorldImagery,
                   group="Two") %>%
  # add first marker
  addProviderTiles(providers$Esri.WorldImagery,
                   group="Two") %>%
  # add first marker
  addMarkers(data = vol,lng=vol$Longitude, lat=vol$Latitude,
             group="mark1") %>%
  # add second marker
  # add Layer controls
  addLayersControl(baseGroups=c("One", "two"),
                   overlayGroups=c("mark1","mark2"),
                   options=layersControlOptions(collapsed=FALSE)) 


