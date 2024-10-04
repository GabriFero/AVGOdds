import json
import httpx
import os
from dotenv import load_dotenv
from multiprocessing import Process
import time

# Carica le variabili d'ambiente dal file .env
env_path = os.path.join(os.getcwd(), "CLOUDBET", "api_key.env")
load_dotenv(env_path)

# Recupera la chiave API
api_key = os.getenv("API_KEY")

# URL per i vari sport
urls = {
    'basketball': 'https://sports-api.cloudbet.com/pub/v2/odds/events?sport=basketball&live=true&players=false&limit=10000',
    'tennis': 'https://sports-api.cloudbet.com/pub/v2/odds/events?sport=tennis&live=true&players=false&limit=10000',
    'football': 'https://sports-api.cloudbet.com/pub/v2/odds/events?sport=soccer&live=true&players=false&limit=10000',
    'pingpong': 'https://sports-api.cloudbet.com/pub/v2/odds/events?sport=table-tennis&live=true&players=false&limit=10000'
}

# Headers per la richiesta
headers = {
    "accept": "application/json",
    "X-API-Key": api_key
}

# Lista di mercati di interesse basati sui params
params_of_interest = ['handicap', 'total', 'winner', '1x2', 'over', 'under']

# Funzione per effettuare la richiesta e salvare i dati "processed" e "non-processed"
def fetch_and_process(sport_name, url):
    try:
        # Richiesta HTTP
        response = httpx.get(url, headers=headers)
        response.raise_for_status()  # Solleva un'eccezione per status code non 2xx
        data = response.json()

        # Salva i dati non processati (raw)
        raw_file_path = os.path.join(os.getcwd(), "CLOUDBET", f"Raw{sport_name.capitalize()}.json")
        with open(raw_file_path, "w", encoding="utf-8") as raw_file:
            json.dump(data, raw_file, indent=4)

        # Estrazione dei dati direttamente dalla risposta
        matches = []
        if 'competitions' in data:
            for competition in data['competitions']:
                for event in competition['events']:
                    # Formatta il nome della partita
                    match_name = event['home']['name'] + " vs " + event['away']['name']
                    for market_name, market_data in event['markets'].items():
                        for submarket_name, submarket_data in market_data['submarkets'].items():
                            for selection in submarket_data['selections']:
                                params = selection.get('params', '')
                                # Filtra in base a "params"
                                if any(keyword in params for keyword in params_of_interest):
                                    matches.append({
                                        'match': match_name,
                                        'market': market_name,
                                        'outcome': selection.get('outcome', 'N/A'),
                                        'params': params,
                                        'price': selection.get('price', 'N/A')
                                    })

        # Salva i dati elaborati (processed)
        processed_file_path = os.path.join(os.getcwd(), "CLOUDBET", f"Processed{sport_name.capitalize()}.json")
        with open(processed_file_path, "w", encoding="utf-8") as processed_file:
            json.dump(matches, processed_file, indent=4)

        print(f"Dati non processati salvati per {sport_name} in {raw_file_path}")
        print(f"Dati elaborati e salvati per {sport_name} in {processed_file_path}")
    
    except httpx.HTTPStatusError as e:
        print(f"Errore HTTP per {sport_name}: {e.response.status_code}")
    except json.JSONDecodeError:
        print(f"Errore nel decodificare la risposta JSON per {sport_name}")
    except Exception as e:
        print(f"Errore imprevisto per {sport_name}: {e}")

if __name__ == "__main__":
    while True:
        cycle_start_time = time.time()
        processes = []
        
        for sport_name, url in urls.items():
            # Crea un processo per ogni richiesta
            p = Process(target=fetch_and_process, args=(sport_name, url))
            processes.append(p)
            p.start()

        # Attende che tutti i processi terminino
        for p in processes:
            p.join()

        print("Tutte le richieste sono state completate e i dati sono stati elaborati e salvati!")
        cycle_end_time = time.time()
        cycle_duration = cycle_end_time - cycle_start_time
        print(f"TEMPO ESECUZIONE CICLO: {cycle_duration:.2f} secondi")
        
        # Attendere un periodo di tempo prima di ripetere il ciclo (ad esempio 60 secondi)
        time.sleep(60)
