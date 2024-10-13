import asyncio
import time
import os
import json

from EUROBET.eurobet import get_match, get_odds
from CLOUDBET.cloudbet import fetch_and_process
from COMPARATOR.compare_odds import compare_odds, save_comparison_results

cloudbet_urls = {
    'basketball': 'https://sports-api.cloudbet.com/pub/v2/odds/events?sport=basketball&live=true&players=false&limit=10000',
    'tennis': 'https://sports-api.cloudbet.com/pub/v2/odds/events?sport=tennis&live=true&players=false&limit=10000',
    'football': 'https://sports-api.cloudbet.com/pub/v2/odds/events?sport=soccer&live=true&players=false&limit=10000',
    'pingpong': 'https://sports-api.cloudbet.com/pub/v2/odds/events?sport=table-tennis&live=true&players=false&limit=10000'
}

async def main():
    while True:
        cycle_start_time = time.time()

        # Start asynchronous tasks for Cloudbet data fetching
        cloudbet_tasks = [fetch_and_process(sport_name, url) for sport_name, url in cloudbet_urls.items()]
        # Start the task to get Eurobet URLs
        get_eurobet_urls_task = asyncio.create_task(get_match())

        # Run Cloudbet tasks and get_match concurrently
        cloudbet_results = await asyncio.gather(*cloudbet_tasks)
        eurobet_urls = await get_eurobet_urls_task

        # Start fetching Eurobet odds after obtaining the URLs
        eurobet_results = await get_odds(eurobet_urls)

        # Process Cloudbet results (list of lists) into a single list
        all_cloudbet_matches = [match for matches in cloudbet_results if matches for match in matches]
        # Ensure eurobet_results is a list
        all_eurobet_matches = eurobet_results if eurobet_results else []

        # Save Cloudbet data
        cloudbet_file_path = os.path.join(os.getcwd(), "CLOUDBET", "ProcessedAllSports.json")
        os.makedirs(os.path.dirname(cloudbet_file_path), exist_ok=True)
        with open(cloudbet_file_path, "w", encoding="utf-8") as cloudbet_file:
            json.dump(all_cloudbet_matches, cloudbet_file, indent=4)

        # Save Eurobet data
        eurobet_file_path = os.path.join(os.getcwd(), "EUROBET", "filtered_odds.json")
        os.makedirs(os.path.dirname(eurobet_file_path), exist_ok=True)
        with open(eurobet_file_path, "w", encoding="utf-8") as eurobet_file:
            json.dump(all_eurobet_matches, eurobet_file, indent=4)

        print("All data has been processed and saved!")
        print(f"Cloudbet data saved in {cloudbet_file_path}")
        print(f"Eurobet data saved in {eurobet_file_path}")

        # Markets of interest
        params_of_interest = [
            '1X2', 'U/O GOAL', 'T/T HANDICAP', 'U/O (INCL. TS)', 'T/T HANDICAP 1T', 'T/T HANDICAP 2T',
            '1Q', '2Q', '3Q', '4Q', 'U/O 1T', 'U/O 2T', 'U/O 1Q', 'U/O 2Q', 'U/O 3Q', 'U/O 4Q',
            'T/T (ESCL. RITIRO)', 'T/T GAME', 'U/O GAME NEL SET', 'GAME NEL SET',
            'T/T MATCH', 'U/O PUNTI SET', 'T/T'
        ]

        # Compare odds between Cloudbet and Eurobet
        comparison_results = compare_odds(all_cloudbet_matches, all_eurobet_matches, params_of_interest)

        # Save comparison results
        save_comparison_results(comparison_results)

        cycle_end_time = time.time()
        cycle_duration = cycle_end_time - cycle_start_time
        print(f"CYCLE EXECUTION TIME: {cycle_duration:.2f} seconds")

        # Wait for a period before repeating the cycle (e.g., 60 seconds)
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
