from turtle import clear
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Apro i file CSV che ho elaborato
data = pd.read_csv("Dati_Trasformati.csv")
data2 = pd.read_csv("Dati_Sistemati.csv")

# Codice Paese
codice = data["code"].unique().tolist()

# Paese preso in riferimento
paese = data["paese"].unique().tolist()

#---------------------------------------------------------------------------------------------------#
# L’Indice di Sviluppo Umano (ISU), definito comunemente Human Development Index (HDI),             #
# è un indicatore di sviluppo macroeconomico che costituisce una modalità diversa di valutazione    #
# del benessere di una nazione, perché tiene conto, oltre che del PIL pro-capite,                   #
# anche di altri fattori della società, tra cui la speranza di vita alla nascita,                   #
# il quantitativo di calorie alimentari disponibili pro-capite, la disponibilità di acqua potabile, # 
# il tasso di alfabetizzazione e il tasso di scolarizzazione della popolazione,                     #
# l’accesso ai servizi sanitari e il grado di libertà politica.                                     #
#---------------------------------------------------------------------------------------------------#

# Indice di Sviluppo Umano (ISU)
isu = []

# Casi totali
ctot = [] 

# Morti totali
mtot = []

#----------------------------------------------------------------------------------------------------------------------------------------------#
# Poiché le politiche del governo possono differire in base allo stato di vaccinazione, viene calcolato un indice di rigore per tre categorie: #
# coloro che sono vaccinati, coloro che non sono vaccinati e una media nazionale ponderata in base alla quota di persone vaccinate.            #
#----------------------------------------------------------------------------------------------------------------------------------------------#

# Indice di rigore dei paesi o IRP
irp = []

# Numero totale di popolazione in quella data e luogo preciso
popolazione = data["pop"].unique().tolist()

#------------------------------------------------------------------------------------------------------------------------------------------------------#
# Il PIL è un indicatore del livello del reddito nazionale. Nei confronti internazionali viene utilizzato il PIL a parità di potere di acquisto (PPS)  #
# al fine di eliminare le distorsioni indotte ai differenti livelli dei prezzi: esso è calcolato come la media pesata dei prezzi di un paniere di beni #
# e servizi che sono omogenei, comparabili e rappresentativi di ogni paese membro dell'Unione Europea.                                                 #
#------------------------------------------------------------------------------------------------------------------------------------------------------#

# GDP (Gross Domestic Product) o PIL (Prodotto Interno Lordo)
pil = []

# Raccolgo le informazioni e le elaboro
for i in paese:
    isu.append((data.loc[data["paese"] == i, "isu"]).sum()/294)
    ctot.append((data2.loc[data2["loc"] == i, "ctot"]).sum())
    mtot.append((data2.loc[data2["loc"] == i, "mtot"]).sum())
    irp.append((data.loc[data["paese"] == i, "irp"]).sum()/294)
    popolazione.append((data2.loc[data2["loc"] == i, "pop"]).sum()/294)
dati_agganciati = pd.DataFrame(list(zip(codice, paese, isu, ctot, mtot, irp, popolazione)),
                               columns = ["Codice Paese", "Paese", "Indice Sviluppo Umano", 
                                          "Casi Totali", "Morti Totali", 
                                          "Indice Rigore Paesi", "Popolazione"])
data = dati_agganciati.sort_values(by=["Casi Totali"], ascending=False)

# Top 10 città fine 2019 inzio 2020
data = data.head(10)
data["PIL prima del Covid-19"] = [65279.53, 8897.49, 2100.75, 
                            11497.65, 7027.61, 9946.03, 
                            29564.74, 6001.40, 6424.98, 42354.41]
data["PIL durante il Covid-19"] = [63543.58, 6796.84, 1900.71, 
                            10126.72, 6126.87, 8346.70, 
                            27057.16, 5090.72, 5332.77, 40284.64]

# Top paese con più morti Covid-19
fig = px.bar(data, x="Morti Totali", y="Paese",
             hover_data=["Paese", "Morti Totali"], 
             color="Indice Sviluppo Umano", height=1000, 
             title="Paesi con il maggior numero di morti per Covid-19")
fig.update_layout(barmode="group", xaxis_tickangle=-45, xaxis_title="Morti Totali", yaxis_title="Paese")
fig.show()

# Top paese con più casi Covid-19
fig = px.bar(data, x="Casi Totali", y="Paese",
             hover_data=["Paese", "Morti Totali"], 
             color="Indice Sviluppo Umano", height=1000, 
             title="Paesi con il maggior numero di casi Covid-19")
fig.update_layout(barmode="group", xaxis_tickangle=-45, xaxis_title="Casi Totali", yaxis_title="Paese")
fig.show()

# Compariamo il numero totale di casi con il numero totale di morti di tutti i Paesi:
fig = go.Figure()
fig.add_trace(go.Bar(
    x=data["Paese"],
    y=data["Casi Totali"],
    name="Casi Totali",
    marker_color="LightSkyBlue"
))
fig.add_trace(go.Bar(
    x=data["Paese"],
    y=data["Morti Totali"],
    name="Morti Totali",
    marker_color="FireBrick"
))
fig.update_layout(barmode="group", xaxis_tickangle=-45, xaxis_title="Paese")
fig.show()

# Percentuale di casi totali e morti totali
casi = data["Casi Totali"].sum()
deceased = data["Morti Totali"].sum()
labels = ["Casi Totali", "Morti Totali"]
values = [casi, deceased]

fig = px.pie(data, values=values, names=labels, 
             title="Casi Totali e Morti Totali in percentuale", hole=0.5)
fig.show()

# Ratio di morte dei Casi di Covid-19
death_rate = (data["Morti Totali"].sum() / data["Casi Totali"].sum()) * 100
("Death Rate = ", death_rate)

#--------------------------------------------------------------------------------------------------------------------------------#
# IRP è una misura composita degli indicatori di risposta, tra cui la chiusura di scuole, luoghi di lavoro, e divieti di viaggio #
# che mostra quanto rigorosamente i paesi stiano seguendo queste misure per controllare la diffusione del Covid-19.              # 
#--------------------------------------------------------------------------------------------------------------------------------#

# Indice Rigore Paesi durante il Covid-19 
fig = px.bar(data, x="Paese", y="Casi Totali",
             hover_data=["Popolazione", "Morti Totali"],
             color="Indice Rigore Paesi", height=1000, 
             title= "Indice Rigore Paesi durante il Covid-19")
fig.show()

#------------------------------------------------------------------------------------------------#
# L"India si comporta molto bene nell"indice di rigore dei paesi durante il focolaio di Covid-19 #
#------------------------------------------------------------------------------------------------#

# Covid-19 impatti sull"economia. 
# Pil procapite prima del focolaio di Covid-19 tra i Paesi con il maggior numero di casi:
fig = px.bar(data, x="Paese", y="Casi Totali",
             hover_data=["Popolazione", "Morti Totali"], 
             color="PIL prima del Covid-19", height=1000, 
             title="PIL procapite prima del Covid-19")
fig.show()

# Pil procapite durante la crescita dei casi di Covid-19:
fig = px.bar(data, x="Paese", y="Casi Totali",
             hover_data=["Popolazione", "Morti Totali"], 
             color="PIL durante il Covid-19", height=1000, 
             title="PIL procapite durante il Covid-19")
fig.show()

# PIL procapite prima e durante il Covid-19, così da notare l"impatto:
fig = go.Figure()
fig.add_trace(go.Bar(
    x=data["Paese"],
    y=data["PIL prima del Covid-19"],
    name="PIL procapite prima del Covid-19",
    marker_color="forestgreen"
))
fig.add_trace(go.Bar(
    x=data["Paese"],
    y=data["PIL durante il Covid-19"],
    name="PIL procapite durante il Covid-19",
    marker_color="steelblue"
))
fig.update_layout(barmode="group", xaxis_tickangle=-45)
fig.show()

#-----------------------------------------------------------------------------------------------#
# Si nota una caduta del PIL procapite in tutti i paesi con un numero maggiore di casi Covid-19 #
#-----------------------------------------------------------------------------------------------#

# Paesi che spendevano le loro ricchezze per lo sviluppo Umano:
fig = px.bar(data, x="Paese", y="Casi Totali",
             hover_data=["Popolazione", "Morti Totali"], 
             color="Indice Sviluppo Umano", height=1000, 
             title="Indice Sviluppo Umano durante il Covid-19")
fig.show()

#-------------------------------------------------------------------------------------------------------------------#
# Ho studiato la diffusione del Covid-19 tra i paesi e il suo impatto sull"economia globale.                        #
# Ho visto che lo scoppio del Covid-19 ha provocato il maggior numero di casi Covid-19 e decessi negli Stati Uniti. #
# Uno dei motivi principali alla base di ciò è l"IRP degli Stati Uniti.                                             #
# È relativamente in base  allla Popolazione.                                                                       #
# Ho anche analizzato come è stato influenzato il PIL pro capite di ogni Paese durante l"epidemia di Covid-19.      #
# Puoi scaricare il dataset originale da qui: https://data.mendeley.com/datasets/b2wvnbnpj9/1                       #
#-------------------------------------------------------------------------------------------------------------------#