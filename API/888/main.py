import orjson
import time
from football import *
from basket import *
from pingpong import *
from tennis import *
import ujson
import asyncio
import aiohttp

headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "it,it-IT;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,pt-BR;q=0.5,pt;q=0.4",
    "origin": "https://www.888sport.it",
    "referer": "https://www.888sport.it/",
    "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/128.0.0.0"
}

async def main():
    while True:
        cycle_start_time = time.time()

        # Ottieni i match in modo sincrono
        football = get_matchF(headers)
        basket = get_matchB(headers)
        tennis = get_matchT(headers)
        pingpong = get_matchP(headers)

        # Processa i match se disponibili
        if football and basket:
            Fmatch = process_matchF(football)
            Fmatchlen = len(Fmatch)
            Bmatch = process_matchB(basket)
            Bmatchlen = len(Bmatch)
            Tmatch = process_matchT(tennis)
            Tmatchlen = len(Tmatch)
            Pmatch = process_matchP(pingpong)
            Pmatchlen = len(Pmatch)

            print(f'NUMERO EVENTI CALCIO: {Fmatchlen}')
            print(f'NUMERO EVENTI BASKET: {Bmatchlen}')
            print(f'NUMERO EVENTI TENNIS: {Tmatchlen}')
            print(f'NUMERO EVENTI PINGPONG: {Pmatchlen}')
            
            print(f'\nID FOOTBALL: {Fmatch}')
            print(f'ID BASKET: {Bmatch}')
            print(f'ID TENNIS: {Tmatch}')
            print(f'ID PINGPONG: {Pmatch}')

            # Esegui tutte le chiamate get_oddsF, get_oddsB, get_oddsT, get_oddsP in parallelo
            Fodds, Bodds, Todds, Podds = await asyncio.gather(
                get_oddsF(Fmatch, headers),
                get_oddsB(Bmatch, headers),
                get_oddsT(Tmatch, headers),
                get_oddsP(Pmatch, headers)
            )

            # Salva i risultati nei file JSON usando ujson
            with open(f"{os.getcwd()}\\API\\888\\FOODS.json", "w", encoding="utf-8") as file:
                file.write(ujson.dumps(Fodds, indent=4))

            with open(f"{os.getcwd()}\\API\\888\\BOODS.json", "w", encoding="utf-8") as file:
                file.write(ujson.dumps(Bodds, indent=4))

            with open(f"{os.getcwd()}\\API\\888\\TOODS.json", "w", encoding="utf-8") as file:
                file.write(ujson.dumps(Todds, indent=4))

            with open(f"{os.getcwd()}\\API\\888\\POODS.json", "w", encoding="utf-8") as file:
                file.write(ujson.dumps(Podds, indent=4))

        # Calcola il tempo di esecuzione del ciclo
        cycle_end_time = time.time()
        cycle_duration = cycle_end_time - cycle_start_time
        print(f"TEMPO ESECUZIONE CICLO: {cycle_duration:.2f} secondi")

        # Aspetta un po' prima di eseguire di nuovo il ciclo, se necessario
        await asyncio.sleep(1)  # Attendi 1 secondo prima di ripetere

if __name__ == "__main__":
    asyncio.run(main())
    
