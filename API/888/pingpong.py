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
tot_pingpong_match = 'https://eu-offering-api.kambicdn.com/offering/v2018/888it/listView/table_tennis/all/all/all.json?lang=it_IT&market=IT&useCombined=true&useCombinedLive=true'



def get_matchP(headers):
    response = clt.get(url=tot_pingpong_match, headers=headers)
    
    if response.status_code == 200:
        
        data = response.json()
        return data
    else:
        print(f"Errore nella richiesta: {response.status_code}")
        return None


def process_matchP(data):
    football = []

    for event_item in data['events']:
        if event_item['event']['state'] == 'STARTED':
            football.append(event_item['event']['id'])  
    
    return football



