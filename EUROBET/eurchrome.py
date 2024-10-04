import json
import time
import undetected_chromedriver as uc
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

url = "https://www.eurobet.it/live-homepage-service/sport-schedule/services/live-homepage/live?prematch=0&live=1"
output_file = "response_data.json"  # Nome del file JSON dove salvare i dati completi

# Definizione dei file di output per ogni disciplineCode (sia non processato che processato)
output_files = {
    1: {'raw': 'RawCalcio.json', 'processed': 'ProcessedCalcio.json'},
    2: {'raw': 'RawBasket.json', 'processed': 'ProcessedBasket.json'},
    3: {'raw': 'RawPallavolo.json', 'processed': 'ProcessedPallavolo.json'},
    60: {'raw': 'RawPingpong.json', 'processed': 'ProcessedPingpong.json'}
}

def initialize_driver():
    # Set up Chrome options
    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-notifications")
    options.add_argument('--disable-gpu')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-popup-blocking')

    # Initialize the driver
    driver = uc.Chrome(options=options)
    return driver

def fetch_data(driver):
    try:
        driver.get(url)  # Visita l'URL
        
        # Aspetta che la pagina carichi completamente
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(("tag name", "pre")))
        
        # Estrai il contenuto della pagina
        page_source = driver.page_source
        
        # Estrai solo il JSON dal tag <pre>
        start_index = page_source.find("<pre>") + len("<pre>")
        end_index = page_source.find("</pre>")
        
        json_string = page_source[start_index:end_index]
        
        # Converti la stringa JSON in un oggetto Python
        return json.loads(json_string)

    except Exception as e:
        print("ERRORE GENERALE:", e)
        return None

def save_to_json(data, filename):
    if data:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Dati salvati in {filename}")

def extract_filtered_data(data):
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        # Dati "raw" e "processed" per ogni disciplina
        filtered_data = {1: {'raw': [], 'processed': []}, 2: {'raw': [], 'processed': []},
                         3: {'raw': [], 'processed': []}, 60: {'raw': [], 'processed': []}}

        for item in data["result"]["itemList"]:
            for event in item.get("itemList", []):
                event_info = event["eventInfo"]
                discipline_code = event_info["disciplineCode"]

                # Filtra solo i disciplineCode di interesse
                if discipline_code in filtered_data:
                    # Aggiungi i dati "raw" (non processati)
                    filtered_data[discipline_code]['raw'].append(event)

                    # Estrai e salva solo i dati processati di interesse
                    bet_groups = event.get("betGroupList", [])

                    # Scorri i gruppi di scommesse per ottenere betCode e additionalInfo
                    for bet_group in bet_groups:
                        for odd in bet_group.get("oddGroupList", []):
                            for odd_item in odd.get("oddList", []):
                                # Estrai i dati desiderati
                                entry = {
                                    "home": event_info["teamHome"]["description"],
                                    "away": event_info["teamAway"]["description"],
                                    "sport_id": event_info["disciplineCode"],
                                    "koef": odd_item["oddValue"] / 100,  # Calcola la quota da oddValue
                                    "diff": 1,  # Valore statico
                                    "d0": event_info["programCode"],  # programCode
                                    "d1": event_info["eventCode"],  # eventCode
                                    "d2": odd_item["betCode"],  # betCode
                                    "d3": odd_item["additionalInfo"],  # additionalInfo
                                    "d4": odd_item["resultCode"],  # resultCode
                                    "bookmaker_event_name": event_info["eventDescription"],
                                    "bookmaker_league_name": event_info["meetingDescription"],
                                    "event_id": event_info["eventCode"],
                                    "bookmaker_id": 106,  # Valore statico
                                    "bk_direct_link": event_info["aliasUrl"],
                                }

                                # Aggiungi l'elemento ai dati filtrati corrispondenti alla disciplina
                                filtered_data[discipline_code]['processed'].append(entry)
    except Exception as e:
        print(f"Errore imprevisto: {e}")

    return filtered_data

def main():
    driver = initialize_driver()  # Inizializza il driver all'inizio

    try:
        while True:
            # Recupera i dati
            data = fetch_data(driver)
            if data:
                # Estrai i dati filtrati
                filtered_data = extract_filtered_data(data)

                # Salva sia i dati "raw" che i dati "processed" per ogni disciplina
                for discipline_code, files in output_files.items():
                    if filtered_data[discipline_code]['raw']:  # Salva solo se ci sono dati "raw"
                        save_to_json(filtered_data[discipline_code]['raw'], files['raw'])
                    if filtered_data[discipline_code]['processed']:  # Salva solo se ci sono dati "processed"
                        save_to_json(filtered_data[discipline_code]['processed'], files['processed'])
            else:
                print("Nessun dato recuperato.")

            # Aspetta un intervallo specificato prima della prossima richiesta (ad esempio, 60 secondi)
            time.sleep(1)  # Puoi aumentare questo valore se necessario
    except KeyboardInterrupt:
        print("Interruzione da tastiera ricevuta, chiusura del programma.")
    finally:
        driver.quit()  # Chiudere il driver alla fine

if __name__ == "__main__":
    main()
