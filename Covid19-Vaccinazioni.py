import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.offline as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

# Importo il dataset
data = pd.read_csv("Vaccini.csv")
data_df = pd.read_csv("Vaccini_Aggiornato.csv") #29 marzo 2022
data.head()

# Esplorazione dei dati e correzzione non c'è più bisogno di eseguire queste righe:
data.describe()
pd.to_datetime(data.Data)
data.Paese.value_counts()

# Facendo delle ricerche su questo dataset ho scoperto che England, Scotland Wales e Northern Ireland sono stati messi separatamente quando fanno tutti parte dell'United Kingdom.
data = data[data.Paese.apply(lambda x: x not in ["England", "Scotland", "Wales", "Northern Ireland"])]
data.Paese.value_counts()
data.Vaccini.value_counts()

# Creo un nuovo DataFrame selezionando i vaccini e la colonna dei paesi separando i vaccini per paese che li utilizza.
df = data[["Vaccini", "Paese"]]
df.head()


# Separando i Paesi in base ai vaccini mensionati.
dict_ = {}
for i in df.Vaccini.unique():
  dict_[i] = [df["Paese"][j] for j in df[df["Vaccini"]==i].index]

vaccini = {}
for key, value in dict_.items():
  vaccini[key] = set(value)
for i, j in vaccini.items():
  print(f"{i}:>>{j}")

# 1° Visualizzazione:
Vaccini_map = px.choropleth(data, locations = 'Codice_ISO', color = 'Vaccini')
Vaccini_map.update_layout(height=215, margin={"r":0,"t":0,"l":0,"b":0})
Vaccini_map.show()

# 2° Visualizzazione:
Paese_Vaccini = data_df.groupby(["Paese", "Codice_ISO", "Vaccini"])['Vaccinazioni_totali', 'Vaccinazioni_totali_in_percentuale', 'Vaccinazioni_giornaliere', 'Vaccinazioni_giornaliere_per_milione', 'Persone_vaccinate', 'Persone_vaccinate_in_percentuale', 'Persone_completamente_vaccinate', 'Persone_completamente_vaccinate_in_percentuale'].max().reset_index()

trace = go.Choropleth(
            locations = Paese_Vaccini['Paese'],
            locationmode='country names',
            z = Paese_Vaccini['Vaccinazioni_giornaliere'],
            text = Paese_Vaccini['Paese'],
            autocolorscale =False,
            reversescale = True,
            colorscale = 'inferno',
            marker = dict(
                line = dict(
                    color = 'rgb(0,0,0)',
                    width = 0.5)
            ),
            colorbar = dict(
                title = 'Media vaccinazioni giornaliere',
                tickprefix = '')
        )

data = [trace]
layout = go.Layout(
    title = 'Vaccinazioni giornaliere per Paese',
    geo = dict(
        showframe = True,
        showlakes = False,
        showcoastlines = True,
        projection = dict(
            type = 'natural earth'
        )
    )
)

fig = dict( data=data, layout=layout )
iplot(fig)

# 3° Visualizzazione
trace = go.Choropleth(
            locations = Paese_Vaccini['Paese'],
            locationmode='country names',
            z = Paese_Vaccini['Persone_vaccinate'],
            text = Paese_Vaccini['Paese'],
            autocolorscale =False,
            reversescale = True,
            colorscale = 'inferno',
            marker = dict(
                line = dict(
                    color = 'rgb(0,0,0)',
                    width = 0.5)
            ),
            colorbar = dict(
                title = 'Persone vaccinate',
                tickprefix = '')
        )

data = [trace]
layout = go.Layout(
    title = 'Persone vaccinate per Paese',
    geo = dict(
        showframe = True,
        showlakes = False,
        showcoastlines = True,
        projection = dict(
            type = 'natural earth'
        )
    )
)

fig = dict( data=data, layout=layout )
iplot(fig)
