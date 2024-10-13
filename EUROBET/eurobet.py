import json
import asyncio
import httpx

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5",
    "Alt-Used": "www.eurobet.it",
    "Connection": "keep-alive",
    "Cookie": "showSplash=false; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Oct+10+2024+05%3A21%3A29+GMT-0400+(Eastern+Daylight+Time)&version=202403.2.0&browserGpcFlag=0&isIABGlobal=false&consentId=577f5c8c-4f86-4e44-9d9a-ecf89fe87d28&interactionCount=2&isAnonUser=1&landingPath=NotLandingPage&AwaitingReconsent=false&groups=C0001%3A1%2CC0004%3A1%2CBG143%3A1%2CC0002%3A1%2CBG144%3A1%2CC0003%3A1&hosts=H9%3A1%2CH67%3A1%2CH81%3A1%2CH100%3A1%2CH208%3A1%2CH301%3A1%2CH331%3A1%2CH340%3A1%2CH351%3A1%2CH353%3A1%2CH572%3A1&genVendors...id=#o-4E1B-eu1#5b63c025-41df-45c5-b7bf-cf855172115e:8dd7526d-bab3-4cc3-a327-d136ca095ac6:1728552047067::1#/1759573947; __cflb=02DiuH88gCYcfmbdqvRW8q67nBKAuELTXFP27syfhUXUx; __cf_bm=wO1PudsOFhcValeIIzbV.eTD7.Xkh2vw3OMdYIXoJBQ-1728552018-1.0.1.1-8qmvDpkTXE8_xepBMiIK_fbW14tdlqSlGOFum9Zx2qkhd8O8WWir.g4oupjFC6KFNervJytBWp.J0uqogC9W8w; kndctr_45F10C3A53DAEC9F0A490D4D_AdobeOrg_cluster=irl1; mboxEdgeCluster=37; fs_lua=1.1728552047067; OptanonAlertBoxClosed=2024-10-10T09:21:29.289Z; _gcl_au=1.1.555916277.1728552089",
    "Host": "www.eurobet.it",
    "If-Modified-Since": "Thu, 10 Oct 2024 09:21:30 GMT",
    "Referer": "https://www.eurobet.it/it/scommesse-live/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "TE": "trailers",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "X-EB-Accept-Language": "it_IT",
    "X-EB-MarketId": "5",
    "X-EB-PlatformId": "1"
}

headers_odds = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5",
    "Alt-Used": "www.eurobet.it",
    "Connection": "keep-alive",
    "Cookie": "Cache-Score=0; x-workers-client-ip=37.161.75.137; showSplash=false; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Oct+06+2024+10%3A10%3A55+GMT-0400+(Eastern+Daylight+Time)&version=202403.2.0&browserGpcFlag=0&isIABGlobal=false&consentId=577f5c8c-4f86-4e44-9d9a-ecf89fe87d28&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&AwaitingReconsent=false&groups=C0001%3A1%2CBG143%3A0%2CC0004%3A0%2CBG144%3A0%2CC0002%3A0%2CC0003%3A0&hosts=H9%3A0%2CH67%3A0%2CH81%3A0%2CH100%3A0%2CH208%3A0%2CH301%3A0%2CH331%3A0%2CH3...; fs_uid=#o-4E1B-eu1#5b63c025-41df-45c5-b7bf-cf855172115e:7b08a56e-156b-42b8-a5c8-0b949be76297:1728223622122::2#/1759573943; __cflb=0H28vh85bCouEVnZz6wL8isJ81w1C5SPVmwcHwuDqyv; __cf_bm=053UdwF_6PIORkz4wQ._VcLqo3dwIKaaNG.DBeUvwLE-1728223605-1.0.1.1-7den4aJZRXhnKti2OmvAbAha2EpbE8TcYHQOWjQlhdywm78Lngh7Z8pMdsljZMJlY8cb57NWSAh1rB5FdKJfQQ; kndctr_45F10C3A53DAEC9F0A490D4D_AdobeOrg_cluster=irl1; mboxEdgeCluster=37; fs_lua=1.1728223843376",
    "Host": "www.eurobet.it",
    "If-Modified-Since": "Sun, 06 Oct 2024 14:14:04 GMT",
    "Referer": "https://www.eurobet.it/it/scommesse-live/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "TE": "trailers",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "X-EB-Accept-Language": "it_IT",
    "X-EB-MarketId": "5",
    "X-EB-PlatformId": "1"
}



async def get_match():
    url = "https://www.eurobet.it/live-homepage-service/sport-schedule/services/live-homepage/live?prematch=0&live=1"
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            #with open('ODDSJSON.json', 'w', encoding='utf-8') as f:
            #    json.dump(data, f, ensure_ascii=False, indent=4)
        else:
            print(f"Errore nella richiesta: Status Code {resp.status_code}")
            return None
    except httpx.RequestError as e:
        print(f"Errore nella richiesta: {str(e)}")
        return None

    desired_disciplines = [1, 2, 3, 60]
    filtered_urls = [
        event["breadCrumbInfo"]["fullUrl"]
        for item in data["result"]["itemList"]
        if item.get("disciplineCode") in desired_disciplines
        for event in item["itemList"]
    ]

    #with open('filtered_URLs.json', 'w', encoding='utf-8') as f:
    #    json.dump(filtered_urls, f, ensure_ascii=False, indent=4)

    print("File salvato con successo.")
    return filtered_urls

async def fetch_odds(client, event_url, params_of_interest):
    full_url = f"https://www.eurobet.it/live-detail-service/sport-schedule/services/event{event_url}/tutte?prematch=0&live=1"
    try:
        response = await client.get(full_url, headers=headers_odds)
        if response.status_code == 200:
            data = response.json()
            bet_group_list = data.get("result", {}).get("betGroupList", [])
            results = []
            # Process the bet_group_list
            for bet_group in bet_group_list:
                bet_description = bet_group.get("betDescription", "").strip()
                if bet_description in params_of_interest:
                    for odd_group in bet_group.get("oddGroupList", []):
                        market_description = odd_group.get("oddGroupDescription", "").strip()
                        for odd_item in odd_group.get("oddList", []):
                            filtered_data = {
                                "market": bet_description,
                                "market_description": market_description,
                                "home": data["result"]["eventInfo"].get("teamHome", {}).get("description", ""),
                                "away": data["result"]["eventInfo"].get("teamAway", {}).get("description", ""),
                                "sport_id": data["result"]["eventInfo"].get("disciplineCode", ""),
                                "koef": odd_item.get("oddValue", 0) / 100,
                                "diff": 1,
                                "d0": odd_item.get("programCode", ""),
                                "d1": odd_item.get("eventCode", ""),
                                "d2": odd_item.get("betCode", ""),
                                "d3": odd_item.get("additionalInfo", ""),
                                "d4": odd_item.get("resultCode", ""),
                                "bookmaker_event_name": data["result"]["eventInfo"].get("eventDescription", ""),
                                "bookmaker_league_name": data["result"]["eventInfo"].get("meetingDescription", ""),
                                "event_id": data["result"]["eventInfo"].get("eventCode", ""),
                                "bookmaker_id": 106,
                                "bk_direct_link": data["result"]["eventInfo"].get("aliasUrl", "")
                            }
                            results.append(filtered_data)
            return results
        else:
            print(f"Failed to get data for {event_url}, status code: {response.status_code}")
            return []
    except httpx.RequestError as e:
        print(f"Errore nella richiesta per {event_url}: {e}")
        return []

async def get_odds(urls):
    results = []
    params_of_interest = [
        '1X2', 'U/O GOAL', 'T/T HANDICAP', 'U/O (INCL. TS)', 'T/T HANDICAP 1T', 'T/T HANDICAP 2T',
        '1Q', '2Q', '3Q', '4Q', 'U/O 1T', 'U/O 2T', 'U/O 1Q', 'U/O 2Q', 'U/O 3Q', 'U/O 4Q',
        'T/T (ESCL. RITIRO)', 'T/T GAME', 'U/O GAME NEL SET', 'GAME NEL SET',
        'T/T MATCH', 'U/O PUNTI SET', 'T/T'
    ]

    async with httpx.AsyncClient() as client:
        tasks = [fetch_odds(client, event_url, params_of_interest) for event_url in urls]
        responses = await asyncio.gather(*tasks)

    # Flatten the list of lists into a single list
    for response in responses:
        if response:
            results.extend(response)

    # Save the results to 'filtered_odds.json'
    #with open('filtered_odds.json', 'w', encoding='utf-8') as f:
    #   json.dump(results, f, ensure_ascii=False, indent=4)

    print("File con le quote filtrate salvato con successo come 'filtered_odds.json'.")
    return results

async def main():
    urls = await get_match()
    if urls:
        await get_odds(urls)

if __name__ == "__main__":
    asyncio.run(main())
