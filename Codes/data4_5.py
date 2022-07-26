# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 23:35:13 2022

@author: yujia
"""

import pandas as pd
import plotly
import plotly.express as px
import seaborn as sns
import numpy as np

volcanoes = pd.read_csv("volcano_data_2010.csv")
earthqua = pd.read_csv("database.csv")

## add year_month to volcanoes df
volcanoes["year_month"] = volcanoes["Year"].astype(str) + "-" + volcanoes["Month"].astype(str)
volcanoes["year_month"] = pd.to_datetime(volcanoes["year_month"])
volcanoes["year_month"] = volcanoes["year_month"].dt.to_period("M")#volcanoes["year_month"].apply(lambda x: x.strftime('%Y-%m'))
volcanoes["event"] = "volcano erup"
vol_loc = volcanoes[['Latitude', 'Longitude','year_month','event']]

earthqua["Date"] = pd.to_datetime(earthqua["Date"], utc=True)#.dt.strftime('%Y-%m')
earthqua["year_month"] = earthqua["Date"].dt.to_period("M")#.apply(lambda x: x.strftime('%Y-%m')) 
#earthqua["year_month"] = pd.to_datetime(earthqua["Date"])

earthq_loc = earthqua[['Latitude', 'Longitude','year_month']]


# select the earthquake years
vol_year_month = list(volcanoes["year_month"].unique())
earthq_loc = earthq_loc[earthq_loc['year_month'].isin(vol_year_month)]
earthq_loc["event"] = "earthquake"

combined_df = vol_loc.append(earthq_loc)


# create empty month
dates = pd.DataFrame()
dates["year_month"] = pd.date_range(start='1/1/2010', end='2018-04-30', freq='M').to_period("M")
combined_df = combined_df.merge(dates, on = "year_month", how = 'right')

combined_df["string_date"] = combined_df["year_month"].apply(lambda x: x.strftime('%Y-%m')) 

# fill missing value 
combined_df['event'] = combined_df['event'].fillna('no event')
combined_df.Latitude = combined_df.Latitude.fillna(0)
combined_df.Longitude = combined_df.Longitude.fillna(0)



#### plotting earthquake with volcano eruption
fig = px.scatter_geo(
    combined_df,  # dataframe
    lon = 'Longitude',
    lat = 'Latitude',
    color="event",  # column shown by color
    hover_name="event",  # hover info title
    animation_frame="string_date",  # column animated
    animation_group = "event",
    title="Volcano Eruption and Earthquake from 2010 to 2017",
    #projection="orthographic"
)
fig.show()
fig.write_html("figure7.html")



# drop feature which is inside missing value
volcanoes.drop(['TSU', 'EQ', 'MISSING', 'MISSING_DESCRIPTION', 'DAMAGE_MILLIONS_DOLLARS', 
                'HOUSES_DESTROYED', 'TOTAL_MISSING', 'TOTAL_MISSING_DESCRIPTION', 
                'TOTAL_DAMAGE_MILLIONS_DOLLARS', 'TOTAL_HOUSES_DESTROYED', 'Agent'], 
               inplace=True, axis=1)

# fill in data with mean in which there is a missing value
volcanoes = volcanoes.fillna(volcanoes.median())


###### Plot 2 for volcanoes
fig2 = px.scatter(
    volcanoes,
    x="Country",
    y="TOTAL_DEATHS",
    labels={"TOTAL_DEATHS": "Total deaths",
           "Country": "Country"},
    title = "Total deaths in Each Country 2010 to 2018",
    color = "Country",
    hover_data = ['Year'],
    width=600,
    height=600,
)
fig2.show()
fig2.update_xaxes(categoryorder='total descending')
fig2.write_html("figure8_1.html")

###### Plot 3 for volcanoes
volcanoes.drop(index = [6], inplace = True)
fig3 = px.scatter(
    volcanoes,
    x="Country",
    y="TOTAL_DEATHS",
    labels={"TOTAL_DEATHS": "Total deaths",
           "Country": "Country"},
    title = "Total deaths in Each Country between 2010 to 2018",
    color = "Country",
    hover_data = ['Year'],
    width=600,
    height=600,
)
fig3.update_xaxes(categoryorder='total descending')
fig3.show()
fig3.write_html("figure8_2.html")







