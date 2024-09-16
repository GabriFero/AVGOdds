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


data = get_match(headers)

if data:
    num_started_events, started_events_ids = process_match(data)
    
    print(f"Numero di eventi STARTED: {num_started_events}")
    print("ID degli eventi STARTED:", started_events_ids)



