import json
import time
from football import *
from basket import *
from pingpong import *
from tennis import *


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
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
}

def main():
    while True:
        football = get_matchF(headers)
        basket = get_matchB(headers)
        tennis = get_matchT(headers)
        pingpong = get_matchP(headers)

        if football and basket:
            Fmatch = process_matchF(football)
            Fmatch = len(Fmatch)
            Bmatch = process_matchB(basket)
            Bmatchlen = len(Bmatch)
            Tmatch = process_matchT(tennis)
            Tmatch = len(Tmatch)
            Pmatch = process_matchP(pingpong)
            Pmatch = len(Pmatch)

            print(f'NUMERO EVENTI CALCIO: {Fmatch}')
            print(f'NUMERO EVENTI BASKET: {Bmatchlen}')
            print(f'NUMERO EVENTI TENNIS: {Tmatch}')
            print(f'NUMERO EVENTI PINGPONG: {Pmatch}')

            print(f'\nID BASKET: {Bmatch}')

            Bodds = get_odds(Bmatch, headers)
            with open(f"{os.getcwd()}\\API\\888\\extracted_odds.json", "w", encoding="utf-8") as file:
                    json.dump(Bodds, file, indent=4)
            time.sleep(2)
        

if __name__ == "__main__":
    main()
    
