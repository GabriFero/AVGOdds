import httpx
import pandas as pd
import numpy as np
import json
import time
import os
import ujson
import aiohttp
import asyncio

clt = httpx.Client(http2=True)

#IN QUESTO CASO 888 PROPONE UN API CHE CI DA TUTTE LE PARTITE
#POI DA QUELL'API SI ESTRAGGONO I DATI E SI VA A CERCARE TUTTE LE ODDS NELLE DIVERSE PARTITE


#CALCIO, BASKET, TENNIS E PINGPONG

#CALCIO
tot_football_match = 'https://eu-offering-api.kambicdn.com/offering/v2018/888it/listView/football/all/all/all.json?lang=it_IT&market=IT&useCombined=true&useCombinedLive=true'



def get_matchF(headers):
    response = clt.get(url=tot_football_match, headers=headers)
    
    if response.status_code == 200:
        
        data = response.json()
        return data
    else:
        print(f"Errore nella richiesta: {response.status_code}")
        return None


def process_matchF(data):
    football = []

    for event_item in data['events']:
        if event_item['event']['state'] == 'STARTED':
            football.append(event_item['event']['id'])  
    
    return football


# Funzione per ottenere le quote per ciascun ID di evento
async def fetch_oddsF(session, Id, headers):
    try:
        url = f'https://eu-offering-api.kambicdn.com/offering/v2018/888it/betoffer/event/{Id}.json?lang=it_IT&market=IT'
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                odds_data = await response.json()
                extracted_odds = []
                
                if 'betOffers' in odds_data:
                    for offer in odds_data['betOffers']:
                        criterion_label = offer['criterion']['label']
                        
                        for outcome in offer['outcomes']:
                            if 'odds' in outcome:
                                extracted_odds.append({
                                    'bet_offer_id': offer['id'],  # ID della scommessa
                                    'participant': outcome['label'],  # Nome del partecipante
                                    'odds_decimal': outcome['odds'],  # Quote decimale
                                    'criterion_label': criterion_label  # Label del criterio
                                })
                return Id, extracted_odds
            else:
                print(f"Errore nella richiesta per evento {Id}: {response.status}")
                return Id, []

    except Exception as e:
        print(f"Errore durante l'elaborazione di basket_id {Id}: {e}")
        return Id, []

# Funzione principale asincrona per gestire tutte le richieste
async def get_oddsF(ids, headers):
    all_extracted_odds = {}

    # Creare una sessione aiohttp per le richieste
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_oddsF(session, Id, headers) for Id in ids]  # Creare un task per ogni richiesta
        results = await asyncio.gather(*tasks)  # Eseguire tutte le richieste in parallelo

        # Popolare il dizionario con i risultati
        for Id, extracted_odds in results:
            all_extracted_odds[Id] = extracted_odds

    return all_extracted_odds


