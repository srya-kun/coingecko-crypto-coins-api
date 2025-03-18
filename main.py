import requests
import pandas as pd
import argparse
import json
import os
from datetime import datetime
from typing import List, Dict, Any

# Configuration file
CONFIG_FILE = "config.json"

def load_config() -> Dict[str, Any]:
    """Loads configuration from config.json."""
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {CONFIG_FILE} not found. Creating a default config file.")
        default_config = {
            "api_key": "YOUR_API_KEY",
            "cache_expiry": 3600  # Cache expiry in seconds (1 hour)
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(default_config, f, indent=4)
        print("Please update config.json with your CoinGecko API key.")
        exit()
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {CONFIG_FILE}. Please check the file.")
        exit()

def fetch_coin_data(coin_ids: List[str], config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Fetches current market data for the specified coin IDs from the CoinGecko API."""
    api_url = "https://api.coingecko.com/api/v3/coins/markets"
    vs_currency = "usd"
    all_data = []
    
    for coin_id in coin_ids:
        # Check cache first
        cache_file = f".cache/{coin_id}.json"
        if os.path.exists(cache_file):
            modified_time = os.path.getmtime(cache_file)
            if (datetime.now().timestamp() - modified_time) < config["cache_expiry"]:
                print(f"Loading {coin_id} data from cache...")
                with open(cache_file, "r") as f:
                    data = json.load(f)
                all_data.append(data)
                continue

        print(f"Fetching {coin_id} data from CoinGecko API...")
        params = {
            "vs_currency": vs_currency,
            "ids": coin_id,
            "order": "market_cap_desc",
            "per_page": 100,
            "page": 1,
            "sparkline": False,
            "price_change_percentage": "24h"
        }
        headers = {"x-cg-api-key": config["api_key"]}
        try:
            response = requests.get(api_url, params=params, headers=headers)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            data = response.json()
            if data:
                # Basic data validation
                if not isinstance(data, list):
                    raise ValueError(f"API response for {coin_id} is not a list.")
                if not all(isinstance(item, dict) for item in data):
                    raise ValueError(f"API response for {coin_id} does not contain dictionaries.")

                # Cache the data
                os.makedirs(os.path.dirname(cache_file), exist_ok=True)
                with open(cache_file, "w") as f:
                    json.dump(data[0], f, indent=4)
                all_data.append(data[0])
            else:
                print(f"No data found for coin ID: {coin_id}")
        except requests.exceptions.RequestException as e:
            print(f"API request failed for {coin_id}: {e}")
        except ValueError as e:
            print(f"Data validation error for {coin_id}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred for {coin_id}: {e}")
            
    return all_data

def transform_data(coin_data: List[Dict[str, Any]]) -> pd.DataFrame:
    """Transforms the fetched data into a Pandas DataFrame."""
    df = pd.DataFrame(coin_data)
    # Data transformation/cleaning example (you can add more transformations here)
    if not df.empty:
        df['market_cap'] = df['market_cap'].astype(float)
        df['current_price'] = df['current_price'].astype(float)
        df['volume'] = df['total_volume'].astype(float)
    return df

def write_to_excel(data: Dict[str, pd.DataFrame]) -> None:
    """Writes the data to an Excel file with a sheet for each coin."""
    today_date = datetime.now().strftime("%d-%m-%Y")
    output_file = f"coingecko_data_{today_date}.xlsx"
    
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        for coin_id, df in data.items():
            df.to_excel(writer, sheet_name=coin_id if len(data) == 1 else today_date, index=False)
    print(f"Data written to {output_file}")

def main():
    """Main function to fetch coin data and write it to an Excel file."""
    parser = argparse.ArgumentParser(description="Fetch CoinGecko data and store it in an Excel file.")
    parser.add_argument("coin_ids", nargs="+", help="List of coin IDs (e.g., bitcoin ethereum).")
    args = parser.parse_args()
    coin_ids = args.coin_ids

    config = load_config()

    coin_data = fetch_coin_data(coin_ids, config)
    
    if not coin_data:
        print("No data fetched. Please check the coin IDs and API key.")
        return

    # Create a dictionary to hold dataframes for each coin
    dfs = {}
    for data in coin_data:
        df = transform_data([data])  # transform_data expects a list of dictionaries
        dfs[data['id']] = df

    write_to_excel(dfs)

