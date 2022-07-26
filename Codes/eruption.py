#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
import numpy as np
import plotly
import folium
import matplotlib.pyplot as plt


# In[2]:


eruption = pd.read_csv("erup.csv")
eruption.head()


# In[3]:


vol = pd.read_csv("archive/volcano.csv")
vol.head()


# In[58]:


eruption["VEI5"] = eruption["vei"]^5
new_erup = eruption[['volcano_name','vei','start_year','latitude','longitude','vei_status','startdate','durations_days']].iloc[:1850]
new_erup.dropna(subset =['durations_days'], inplace = True)


# In[59]:


import plotly.express as px
Fig4 = px.scatter_geo(
    new_erup,  # dataframe
    lon = 'longitude',
    lat = 'latitude',
    color="vei_status",  # column shown by color
    hover_name="volcano_name",  # hover info title
    size="vei", 
    hover_data = ['startdate'],
    #animation_frame="start_year",  # column animated
    projection="orthographic",  # type of map
    title="The Spread of Volcanic Explosivity Index After 1800",
    labels={"vei_status": "Measurement of the Relative Explosivity"}
)
Fig4.show()
Fig4.write_html("Fig_4.html")


# In[40]:


# Get max VEI for each volcano
vol_vei = eruption.groupby(['volcano_number'])['vei'].max().reset_index()

# Merge these values into the volcano dataframe
volca = pd.merge(vol, vol_vei, on='volcano_number')
vei_status = eruption[['volcano_number','vei_status']]
volcano = pd.merge(volca, vei_status, on='volcano_number')


# In[41]:


volcano.head()


# In[42]:


def vei_radius(vei):
    return 2 ** (int(vei) - 4) + 3 if not np.isnan(vei) else 1
    
volcano_vei = volcano#.dropna(subset=['vei'])

# Create the map
volcano_vei_map = folium.Map()

# Create layers
layers = []
for i in range(8):
    layers.append(folium.FeatureGroup(name='VEI: '+str(i)))
    layers.append(folium.FeatureGroup(name='VEI: NaN'))

# Add each volcano to the correct layer
for i in range(0, volcano_vei.shape[0]):
    volcano = volcano_vei.iloc[i]
    # Create marker
    marker = folium.CircleMarker([volcano['latitude'],
                                  volcano['longitude']],
                                  popup=volcano['volcano_name'] + ', VEI: ' + str(volcano['vei']),
                                  radius=vei_radius(volcano['vei']),
                                  color="purple",
                                 ##"pink" if not np.isnan(volcano['vei']) and int(volcano['vei']) == 7 else 'purple',
                                  fill=volcano['vei_status'])
    # Add to correct layer
    if np.isnan(volcano['vei']):
        marker.add_to(layers[8])
    else:
        marker.add_to(layers[int(volcano['vei'])])

# Add layers to map
for layer in layers:
    layer.add_to(volcano_vei_map)
folium.LayerControl().add_to(volcano_vei_map)

volcano_vei_map


# In[ ]:


#Here is my contribution to include title to folium maps:
m = folium.Map()

title_html = '''
             <h3 align="center" style="font-size:20px"><b>Your map title</b></h3>
             '''
m.get_root().html.add_child(folium.Element(title_html))

m

