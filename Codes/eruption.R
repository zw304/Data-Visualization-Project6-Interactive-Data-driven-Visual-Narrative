library(dplyr)
library(tidyverse)
library(ggplot2)
library(plotly)

erup <- read.csv("archive/eruptions.csv")
head(erup)

eruption <- erup %>%
  mutate(vei_status =  case_when(vei == 0 ~ 'non explosive',
                                 vei == 1 ~ 'small',
                                 vei >= 2 & vei <= 3 ~ 'moderate',
                                 vei >= 4 & vei <= 5 ~ 'large',
                                 vei >= 6 & vei <= 7 ~ 'very large')) %>%
  dplyr::select(c(1,2,5:9,11:16)) %>%
  na.omit() %>%
  distinct()
  
eruption$startdate <- as.Date(with(eruption,paste(start_year,
                                                  start_month,
                                                  start_day,sep="-")),
                              "%Y-%m-%d")

eruption$enddate <- as.Date(with(eruption,paste(end_year,
                                                  end_month,
                                                  end_day,sep="-")),
                              "%Y-%m-%d")
eruption$durations_days = as.numeric(eruption$enddate - eruption$startdate)
write.csv(eruption,"erup.csv")

##1 area of activity
eruptions <- eruption %>%
  dplyr::select(-c(4:12))

vol <- read.csv("archive/volcano.csv")
aaa <- left_join(eruptions, vol, by="volcano_name") %>%
  na.omit() %>%
  dplyr::select(c(country, vei_status, durations_days))

aa <- aaa %>%
  group_by(country, vei_status) %>%
  summarise(durations_days = mean(durations_days)) %>%
  na.omit()

library(forcats)
p <- aa %>%
  filter(durations_days > 365 & durations_days < 730) %>%
  arrange(desc(durations_days)) %>% 
  ggplot(aes(fct_reorder(country, durations_days), durations_days , size = durations_days, 
             color=vei_status)) +
  geom_point() +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 60)) +
  ggtitle("The Area of Activity Where Volcanic Eruptions Last Between 1-2 Years") +
  xlab("Country") +
  ylab("Duration Days") +
  labs(color = "Measurement of the Relative Explosivity") +
  labs(size='Durations Days') 
  

ggplotly(p)
#library(htmlwidgets)
#saveWidget(p, file="aap.html")

##2 map
library(ggiraph)
library(colormap)
 
world <- map_data("world") %>% 
  rename(longitude = long) %>% 
  rename(latitude = lat) %>% 
  mutate_if(is.numeric, round, 3)

map2 <- eruption %>% left_join(world, by = c("longitude", "latitude"))

ll <- 
  ggplot() +
  geom_map(
    data = world, map = world,
    aes(longitude, latitude, map_id = region),
    color = "white", fill = "gray20", size = 0.01, alpha = 0.1
  ) +
  geom_point(eruption, 
             mapping = aes(longitude, latitude, 
                 size = vei^5,  color=vei_status),
             alpha = 0.4,
  ) +
  theme_bw() +
  scale_fill_gradient() +
  scale_color_hue(direction = 1) + 
  ggtitle("The Spread of Volcanic Explosivity Index") +
  xlab("Longitude") +
  ylab("Latitude")

ggplotly(ll)

library(esquisse)
esquisser()

##3 evidence_category
ec <- erup %>%
  filter(end_year > 1800) %>%
  ggplot(aes(end_year, fill=eruption_category, alpha = 0.5)) +
  geom_density() +
  #facet_wrap(~vei_status, scales = "free") +
  scale_x_continuous(breaks = seq(1800, 2020, 20)) +
  ggtitle("Comparison Between Volcano Eruption Evidence Categories") +
  xlab("Last Eruption Year") +
  ylab("Density")

ggplotly(ec)

##4 volcanos with more active eruptions
vol <- read.csv("archive/volcano.csv")
ae <- left_join(eruption, vol, by="volcano_name") %>%
  na.omit()
active <- ae %>% 
  group_by(country) %>%
  count(volcano_name) %>%
  arrange(-n) %>%
  head(40) %>%
  ggplot(aes(x=reorder(paste(volcano_name, country, sep = " - "), n), 
             y=n)) +
  geom_bar(stat='identity', fill="lightpink") +
  coord_flip() +
  ggtitle("Volcanos With More Active Eruptions") +
  labs(x="Volcano Names",
       y="Number of Eruptions")

ggplotly(active)

