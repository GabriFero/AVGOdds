import requests
import json
import httpx

clt = httpx.Client(http2=True)

url_eurobet = 'https://www.eurobet.it/live-homepage-service/sport-schedule/services/live-homepage/live'

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3",
    "Connection": "keep-alive",
    "Cookie": "__cf_bm=6GvAzZK8JzI99hs0vQkgSmp4vZijodqSRwt94avJtP8-1727016178-1.0.1.1-uKMJ8MG2zgdkPuL7rvdSZc2osDarLb2gBeYM86BQFmtzEsB2qImZ1VnjPKjXNjOcDAYze98a7uMDCL4oiOKegw",
    "Host": "www.eurobet.it",
    "If-Modified-Since": "Sun, 22 Sep 2024 14:42:58 GMT",
    "Priority": "u=0, i",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "TE": "trailers",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0"
}

# Parametri della query string
params = {
    "prematch": 0,
    "live": 1
}

# Effettua la richiesta GET con headers e cookies
response = requests.get(url=url_eurobet, headers=headers, params=params)

# Verifica lo stato della risposta
if response.status_code == 200:
    data = response.json()  # Processa la risposta come JSON
    print(json.dumps(data, indent=4))  # Stampa i dati in modo leggibile
else:
    print(f"Errore: {response.status_code}")
