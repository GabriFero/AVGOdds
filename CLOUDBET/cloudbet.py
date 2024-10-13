import json
import httpx
import os
import asyncio
import time
from dotenv import load_dotenv

# Load environment variables from the .env file
env_path = os.path.join(os.getcwd(), "CLOUDBET", "api_key.env")
load_dotenv(env_path)

# Retrieve the API key
api_key = os.getenv("API_KEY")

# URLs for the various sports
urls = {
    'basketball': 'https://sports-api.cloudbet.com/pub/v2/odds/events?sport=basketball&live=true&players=false&limit=10000',
    'tennis': 'https://sports-api.cloudbet.com/pub/v2/odds/events?sport=tennis&live=true&players=false&limit=10000',
    'football': 'https://sports-api.cloudbet.com/pub/v2/odds/events?sport=soccer&live=true&players=false&limit=10000',
    'pingpong': 'https://sports-api.cloudbet.com/pub/v2/odds/events?sport=table-tennis&live=true&players=false&limit=10000'
}

# Headers for the request
headers = {
    "accept": "application/json",
    "X-API-Key": api_key
}

# List of markets of interest based on params
params_of_interest = ['handicap', 'total', 'winner', '1x2', 'over', 'under']

# Asynchronous function to fetch and process data
async def fetch_and_process(sport_name, url):
    try:
        async with httpx.AsyncClient() as client:
            # Asynchronously send the HTTP request
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

            # Extract data directly from the response
            matches = []
            if 'competitions' in data:
                for competition in data['competitions']:
                    for event in competition['events']:
                        # Format the match name
                        match_name = f"{event['home']['name']} vs {event['away']['name']}"
                        for market_name, market_data in event['markets'].items():
                            for submarket_data in market_data['submarkets'].values():
                                for selection in submarket_data['selections']:
                                    params = selection.get('params', '')
                                    # Filter based on "params"
                                    if any(keyword in params for keyword in params_of_interest):
                                        match_data = {
                                            'sport': sport_name,
                                            'match': match_name,
                                            'market': market_name,
                                            'outcome': selection.get('outcome', 'N/A'),
                                            'params': params,
                                            'price': selection.get('price', 'N/A')
                                        }
                                        matches.append(match_data)

            return matches

    except httpx.HTTPStatusError as e:
        print(f"HTTP error for {sport_name}: {e.response.status_code}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON response for {sport_name}")
    except Exception as e:
        print(f"Unexpected error for {sport_name}: {e}")

    return []

async def main():
    while True:
        cycle_start_time = time.time()
        
        # Create a list of tasks for asynchronous execution
        tasks = [fetch_and_process(sport_name, url) for sport_name, url in urls.items()]
        
        # Run all tasks concurrently
        results = await asyncio.gather(*tasks)
        
        # Flatten the list of lists into a single list
        all_matches = [match for matches in results if matches for match in matches]
        
        # Save all processed data into a single file
        combined_file_path = os.path.join(os.getcwd(), "CLOUDBET", "ProcessedAllSports.json")
        with open(combined_file_path, "w", encoding="utf-8") as combined_file:
            json.dump(all_matches, combined_file, indent=4)
        
        print("All data has been processed and saved!")
        print(f"Data for all sports has been saved in {combined_file_path}")
        
        cycle_end_time = time.time()
        cycle_duration = cycle_end_time - cycle_start_time
        print(f"CYCLE EXECUTION TIME: {cycle_duration:.2f} seconds")
        
        # Wait for a period before repeating the cycle (e.g., 60 seconds)
        await asyncio.sleep(3)

if __name__ == "__main__":
    asyncio.run(main())
