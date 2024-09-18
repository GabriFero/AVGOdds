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
tot_basket_match = 'https://eu-offering-api.kambicdn.com/offering/v2018/888it/listView/basketball/all/all/all.json?lang=it_IT&market=IT&useCombined=true&useCombinedLive=true'




def get_matchB(headers):
    response = clt.get(url=tot_basket_match, headers=headers)
    
    if response.status_code == 200:
        
        data = response.json()  
        return data
    else:
        print(f"Errore nella richiesta: {response.status_code}")
        return None


def process_matchB(data):
    basket = []

    for event_item in data['events']:
        if event_item['event']['state'] == 'STARTED':
            basket.append(event_item['event']['id'])  
    
    return basket


# Funzione per ottenere le quote per ciascun ID di evento
def get_oddsB(ids, headers):
    all_extracted_odds = {} 

    for Id in ids :
        try:
            url = f'https://eu-offering-api.kambicdn.com/offering/v2018/888it/betoffer/event/{Id}.json?lang=it_IT&market=IT'
            
            response = clt.get(url=url, headers=headers)
            
            if response.status_code == 200:
                odds_data = response.json()          
                extracted_odds = []
                
                if 'betOffers' in odds_data:
                    for offer in odds_data['betOffers']:
                        criterion_label = offer['criterion']['label']  
                        
                        for outcome in offer['outcomes']:
                            if 'odds' in outcome:
                                extracted_odds.append({
                                    'bet_offer_id': offer['id'],                     # ID della scommessa
                                    'participant': outcome['label'],                 # Nome del partecipante
                                    'odds_decimal': outcome['odds'],                 # Quote decimale
                                    'criterion_label': criterion_label               # Label del criterio
                                })
                            else:
                                continue

                all_extracted_odds[Id] = extracted_odds
                
            else:
                print(f"Errore nella richiesta per evento {Id}: {response.status_code}")
        
        except Exception as e:
            print(f"Errore durante l'elaborazione di basket_id {Id}: {e}")
    
    return all_extracted_odds
