import pandas as pd
import plotly.express as px
df = pd.read_csv('./data2.csv')
df.head()

#####fig1
df = df.drop(['Currently Erupting (17 March 2022)'], axis=1)
df = df.sort_values(by=['Holocene Volcanoes'])
df.head()

fig1 = px.scatter(df, x="Holocene Volcanoes", y="Active since 1800 CE",
                 size="Active since 1960 CE", color="Country",
                 hover_name="Country", log_x=True, size_max=60,
                  title="Volcanoes' Number in Different Era and Countries")
fig1.write_html("df2_plot.html")
