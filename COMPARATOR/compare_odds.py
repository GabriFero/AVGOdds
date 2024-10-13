import json
import os
import re

# Function to normalize team names for better matching
def normalize_team_name(name):
    name = name.lower()
    name = re.sub(r'[^a-z0-9\s]', '', name)  # Remove special characters
    name = re.sub(r'\s+', ' ', name)  # Replace multiple spaces with a single space
    return name.strip()

# Function to map Cloudbet market names to Eurobet market names
def map_market_name(cloudbet_market, cloudbet_params):
    # Mapping dictionary between Cloudbet and Eurobet market names
    market_mapping = {
        # Football (Soccer)
        'soccer.match.winner.v2': '1X2',
        'soccer.match.total.v2': 'U/O GOAL',
        'soccer.match.total_goals': 'U/O GOAL',  # Added mapping
        'soccer.total_goals': 'U/O GOAL',        # Added mapping
        'soccer.match.handicap.v2': 'T/T HANDICAP',
        'soccer.match.total_incl_ot.v2': 'U/O (INCL. TS)',
        'soccer.first_half.handicap.v2': 'T/T HANDICAP 1T',
        'soccer.second_half.handicap.v2': 'T/T HANDICAP 2T',
        # Basketball
        'basketball.period.winner': {'1': '1Q', '2': '2Q', '3': '3Q', '4': '4Q'},
        'basketball.period.total': {'1': 'U/O 1Q', '2': 'U/O 2Q', '3': 'U/O 3Q', '4': 'U/O 4Q'},
        'basketball.match.total': 'U/O PUNTI SET',
        'basketball.match.handicap': 'T/T HANDICAP',
        # Tennis
        'tennis.match.winner.v2': 'T/T MATCH',
        'tennis.match.handicap.v2': 'T/T (ESCL. RITIRO)',
        'tennis.set.handicap.v2': 'GAME NEL SET',
        'tennis.set.total_games.v2': 'U/O GAME NEL SET',
        # Table Tennis
        'table_tennis.match.winner.v2': 'T/T MATCH',
        'table_tennis.match.handicap.v2': 'T/T GAME',
        'table_tennis.match.total_points.v2': 'U/O PUNTI SET',
        # Add more mappings as needed
    }

    # Get the base market name from the mapping
    base_market = None
    market_description = None

    if cloudbet_market in market_mapping:
        mapping_value = market_mapping[cloudbet_market]

        # Handle markets with periods (quarters, halves)
        if isinstance(mapping_value, dict):
            params_dict = dict(param.split('=') for param in cloudbet_params.split('&') if '=' in param)
            period = params_dict.get('period')
            if period in mapping_value:
                base_market = mapping_value[period]
                market_description = base_market
        else:
            base_market = mapping_value
            market_description = base_market

        # For markets with handicap or total parameters
        params_dict = dict(param.split('=') for param in cloudbet_params.split('&') if '=' in param)
        if 'handicap' in params_dict:
            handicap = params_dict['handicap']
            market_description = handicap  # Use only the handicap value
        elif 'total' in params_dict:
            total = params_dict['total']
            market_description = total  # Use only the total value
    else:
        # Market not found in mapping
        pass

    return base_market, market_description

# Function to compare odds between Cloudbet and Eurobet
def compare_odds(cloudbet_data, eurobet_data, params_of_interest):
    comparison_results = []

    # Create a list of Eurobet events with normalized team names
    eurobet_events = []
    for eurobet_event in eurobet_data:
        home_team = normalize_team_name(eurobet_event.get('home', ''))
        away_team = normalize_team_name(eurobet_event.get('away', ''))
        eurobet_events.append({
            'home': home_team,
            'away': away_team,
            'market': eurobet_event.get('market', ''),
            'market_description': eurobet_event.get('market_description', ''),
            'koef': eurobet_event.get('koef', 0),
            'event': eurobet_event,  # Store the original event data
        })

    # Iterate over Cloudbet events
    for cloudbet_event in cloudbet_data:
        # Normalize team names
        cloudbet_match = cloudbet_event.get('match', '')
        if ' vs ' in cloudbet_match:
            cloudbet_home, cloudbet_away = cloudbet_match.split(' vs ')
        else:
            continue  # Skip if match name format is unexpected
        cloudbet_home = normalize_team_name(cloudbet_home)
        cloudbet_away = normalize_team_name(cloudbet_away)

        # Map Cloudbet market to Eurobet market
        cloudbet_market = cloudbet_event.get('market', '')
        cloudbet_params = cloudbet_event.get('params', '')
        base_market, market_description = map_market_name(cloudbet_market, cloudbet_params)

        if not base_market:
            continue  # Skip if market mapping is not defined

        # Only proceed if the market is in params_of_interest
        if base_market not in params_of_interest:
            continue

        # Try to find matching Eurobet events
        for eurobet_event in eurobet_events:
            # Check if teams match (in any order)
            teams_match = (
                (cloudbet_home == eurobet_event['home'] and cloudbet_away == eurobet_event['away']) or
                (cloudbet_home == eurobet_event['away'] and cloudbet_away == eurobet_event['home'])
            )

            # Check if markets match
            eurobet_market = eurobet_event['market']
            eurobet_market_description = eurobet_event['market_description']

            # For markets with descriptions (e.g., handicaps), compare descriptions
            markets_match = base_market == eurobet_market and market_description == eurobet_market_description

            if teams_match and markets_match:
                eurobet_koef = eurobet_event['koef']
                try:
                    cloudbet_price = float(cloudbet_event.get('price', 0))
                    eurobet_price = float(eurobet_koef)
                    difference = abs(cloudbet_price - eurobet_price)

                    comparison_data = {
                        'match': cloudbet_event['match'],
                        'market': base_market,
                        'market_description': market_description,
                        'cloudbet_price': cloudbet_price,
                        'eurobet_price': eurobet_price,
                        'difference': difference,
                        'cloudbet_outcome': cloudbet_event.get('outcome', ''),
                        'eurobet_outcome': eurobet_event['event'].get('d4', ''),  # Outcome code
                    }
                    comparison_results.append(comparison_data)
                except ValueError:
                    print(f"Error converting prices to float for match {cloudbet_event['match']}")
                break  # Stop searching after finding a match

    return comparison_results

# Function to save comparison results to a JSON file
def save_comparison_results(results):
    comparison_file_path = os.path.join(os.getcwd(), "COMPARATOR", "ComparisonResults.json")
    os.makedirs(os.path.dirname(comparison_file_path), exist_ok=True)
    with open(comparison_file_path, "w", encoding="utf-8") as comparison_file:
        json.dump(results, comparison_file, indent=4)
    print(f"Comparison completed and results saved in {comparison_file_path}")

