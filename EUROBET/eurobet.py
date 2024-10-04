import requests
import brotlicffi

url = "https://www.eurobet.it/live-homepage-service/sport-schedule/services/live-homepage/live"

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",  # 'br' indicates Brotli
    "Accept-Language": "en-US,en;q=0.5",
    "Alt-Used": "www.eurobet.it",
    "Connection": "keep-alive",
    "Cookie": "__cflb=02DiuH88gCYcfmbdqvRW8q67nBKAuELTWRFiSVpmsdo3S; __cf_bm=xLEf8cvXKP6Ed_WYcX04DWf4GPnotu3gBfpNO4Z3.WI-1728037905-1.0.1.1-R6IXfpnGMrvDvOqtNbxjUquZNLk7S7hUpXY5k9Nc4XEOOsNazGtEHqcf1BVjYisJylP.pPcMreG9.3pCRVKCMw; showSplash=false; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Oct+04+2024+06%3A32%3A17+GMT-0400+(Eastern+Daylight+Time)&version=202403.2.0&browserGpcFlag=0&isIABGlobal=false&consentId=577f5c8c-4f86-4e44-9d9a-ecf89fe87d28&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage; ADRUM_BTa=R:41|g:fb2d0f05-cd7b-49e1-97a2-9bb19dfe4ab6|n:customer1_e973bb1a-df13-4259-a051-d70bb42bca23; SameSite=None; ADRUM_BT1=R:41|i:10234|e:6; mbox=session#27627723739532017640255215016728768986-HpgpOU#1728039787; mboxEdgeCluster=37; kndctr_45F10C3A53DAEC9F0A490D4D_AdobeOrg_identity=CiYyNzYyNzcyMzczOTUzMjAxNzY0MDI1NTIxNTAxNjcyODc2ODk4NlITCPfw2LilMhABGAEqBElSTDEwAPAB9_DYuKUy; kndctr_45F10C3A53DAEC9F0A490D4D_AdobeOrg_cluster=irl1",
    "Host": "www.eurobet.it",
    "If-Modified-Since": "Fri, 04 Oct 2024 10:32:19 GMT",
    "Referer": "https://www.eurobet.it/it/scommesse-live/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "TE": "trailers",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "X-EB-Accept-Language": "it_IT",
    "X-EB-MarketId": "5",
    "X-EB-PlatformId": "2",
}

response = requests.get(url, headers=headers)

# Check the Content-Encoding header
content_encoding = response.headers.get('Content-Encoding')
print("Content-Encoding:", content_encoding)

# Handle Brotli response if content-encoding is Brotli
try:
    if content_encoding == 'br':
        response_content = brotlicffi.decompress(response.content)
    else:
        response_content = response.content  # Fallback to raw content
        print("Received raw content (not Brotli):")
        print(response_content[:1000])  # Print the first 1000 bytes of raw content for inspection
except Exception as e:
    print("Error decompressing response:", str(e))
    response_content = response.content  # Fallback to raw content in case of decompression error

# Print the status code and headers
print("Status Code:", response.status_code)
print("Response Headers:", response.headers)
print("Response Content:", response_content.decode('utf-8', errors='replace'))  # Decoding with error handling
