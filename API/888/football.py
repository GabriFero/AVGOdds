import httpx
import pandas as pd
import numpy as np
import json
import time
import os

clt = httpx.Client(http2=True)

#IN QUESTO CASO 888 PROPONE UN API CHE CI DA TUTTE LE PARTITE
#POI DA QUELL'API SI ESTRAGGONO I DATI E SI VA A CERCARE TUTTE LE ODDS NELLE DIVERSE PARTITE


#CALCIO, BASKET, TENNIS E PINGPONG

#CALCIO
tot_football_match = 'https://eu-offering-api.kambicdn.com/offering/v2018/888it/listView/football/all/all/all.json?lang=it_IT&market=IT&useCombined=true&useCombinedLive=true'



def get_match(headers):
    response = clt.get(url=tot_football_match, headers=headers)
    
    if response.status_code == 200:
        
        data = response.json()
        print(data)
        with open(f"{os.getcwd()}\\API\\888\\M888.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)  
        return data
    else:
        print(f"Errore nella richiesta: {response.status_code}")
        return None


def process_match(data):
    started_events = []

    for event_item in data['events']:
        if event_item['event']['state'] == 'STARTED':
            started_events.append(event_item['event']['id'])  # Aggiungi l'ID dell'evento

    num_started_events = len(started_events)
    
    return num_started_events, started_events



