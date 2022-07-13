import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.colors as mcolors
import pandas as pd 
import random
import math
import time
from sklearn.linear_model import LinearRegression, BayesianRidge
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error
import datetime

# importo i dataset
confermati_df = pd.read_csv('time_series_covid19_confirmed_global.csv')
morti_df = pd.read_csv('time_series_covid19_deaths_global.csv')

confermati_df.head()
coll = confermati_df.keys()

confermati = confermati_df.loc[:, coll[4]:coll[-1]]
morti = morti_df.loc[:, coll[4]:coll[-1]]

date = confermati.keys()
casi_nel_mondo = []
morti_totali = [] 
ratio_mortalità = []

for i in date:
    somma_confermati = confermati[i].sum()
    somma_morti = morti[i].sum()
    casi_nel_mondo.append(somma_confermati)
    morti_totali.append(somma_morti)
    ratio_mortalità.append(somma_morti/somma_confermati)

def incremento_giornaliero(data):
    d = [] 
    for i in range(len(data)):
        if i == 0:
            d.append(data[0])
        else:
            d.append(data[i]-data[i-1])
    return d 

def media_movimento(data, window_size):
    media_movimento = []
    for i in range(len(data)):
        if i + window_size < len(data):
            media_movimento.append(np.mean(data[i:i+window_size]))
        else:
            media_movimento.append(np.mean(data[i:len(data)]))
    return media_movimento

window = 7

# Casi confermati
incremento_giornaliero_mondiale = incremento_giornaliero(casi_nel_mondo)
world_confermati_avg= media_movimento(casi_nel_mondo, window)
media_di_incremento_giornaliero_mondiale = media_movimento(incremento_giornaliero_mondiale, window)

# Morti
media_giornaliera_di_morti = incremento_giornaliero(morti_totali)
media_morti_nel_mondo = media_movimento(morti_totali, window)
media_giornaliera_di_morti_nel_mondo = media_movimento(media_giornaliera_di_morti, window)

giorni_dal_01_22_20 = np.array([i for i in range(len(date))]).reshape(-1, 1)
casi_nel_mondo = np.array(casi_nel_mondo).reshape(-1, 1)
morti_totali = np.array(morti_totali).reshape(-1, 1)

days_in_future = 10
future_forcast = np.array([i for i in range(len(date)+days_in_future)]).reshape(-1, 1)
dati_sistemati = future_forcast[:-10]

inizio = '1/22/2020'
data_di_inizio = datetime.datetime.strptime(inizio, '%m/%d/%Y')
data_futura_prevista = []
for i in range(len(future_forcast)):
    data_futura_prevista.append((data_di_inizio + datetime.timedelta(days=i)).strftime('%m/%d/%Y'))

# Modifico i dati per un FIT PERFECT
giorni_da_skippare = 376
X_train_confermati, X_test_confermati, y_train_confermati, y_test_confermati = train_test_split(giorni_dal_01_22_20[giorni_da_skippare:], casi_nel_mondo[giorni_da_skippare:], test_size=0.08, shuffle=False)

#rendo i dati piatti cosi da poterci stare in un Bar-Graph
def flatten(arr):
    a = [] 
    arr = arr.tolist()
    for i in arr:
        a.append(i[0])
    return a

# 1° visualizzazione
dati_sistemati = dati_sistemati.reshape(1, -1)[0]
plt.figure(figsize=(20, 10))
plt.plot(dati_sistemati, casi_nel_mondo)
plt.plot(dati_sistemati, world_confermati_avg, linestyle='dashed', color='purple')
plt.title('Numero di Casi Covid-19 nel tempo', size=30)
plt.xlabel('Giorni dal 1/22/2020 al 7/6/2022', size=30)
plt.ylabel('Numero di casi Covid-19', size=30)
plt.legend(['Casi di Covid-19 in tutto il mondo', 'Media mobile di {} Giorni'.format(window)], prop={'size': 20})
plt.xticks(size=20)
plt.yticks(size=20)
plt.show()

# 2° Visualizzazione
plt.figure(figsize=(20, 10))
plt.plot(dati_sistemati, morti_totali)
plt.plot(dati_sistemati, media_morti_nel_mondo, linestyle='dashed', color='purple')
plt.title('Numero di morti di Covid-19 nel tempo', size=30)
plt.xlabel('Giorni dal 1/22/2020 al 7/6/2022', size=30)
plt.ylabel('Numero di casi Covid-19', size=30)
plt.legend(['Covid-19 morti in tutto il mondo', 'Media mobile di {} Giorni'.format(window)], prop={'size': 20})
plt.xticks(size=20)
plt.yticks(size=20) 
plt.show()

# 3° Visualizzazione
plt.figure(figsize=(20, 10))
plt.bar(dati_sistemati, incremento_giornaliero_mondiale)
plt.plot(dati_sistemati, media_di_incremento_giornaliero_mondiale, linestyle='dashed', color='purple')
plt.title('Incremento di casi Covid-19 giornalieri confermati', size=30)
plt.xlabel('Giorni dal 1/22/2020 al 7/6/2022', size=30)
plt.ylabel('Numero di casi Covid-19', size=30)
plt.legend(['Media mobile di {} Giorni'.format(window), 'Incremento mondiale di casi Covid-19'], prop={'size': 20})
plt.xticks(size=20)
plt.yticks(size=20)
plt.show()

# 4° Visualizzazione
plt.figure(figsize=(20, 10))
plt.bar(dati_sistemati, media_giornaliera_di_morti)
plt.plot(dati_sistemati, media_giornaliera_di_morti_nel_mondo, color='purple', linestyle='dashed')
plt.title('Incremento mondiale di morti per Covid-19 giornalieri confermati', size=30)
plt.xlabel('Conteggio giorni dal 1/22/2020 al 7/6/22', size=30)
plt.ylabel('Numero di casi positivi', size=30)
plt.legend(['Media mobile di {} Giorni'.format(window), 'Incremento mondiale giornaliero di casi Covid-19'], prop={'size': 20})
plt.xticks(size=20)
plt.yticks(size=20)
plt.show()