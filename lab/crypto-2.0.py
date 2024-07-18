import requests
from bs4 import BeautifulSoup
import json
import re

def clean_value(value):
    # Remove percentage change but keep the dollar sign
    cleaned_value = re.sub(r'^[\d.]+%', '', value).strip()
    return cleaned_value

def scrape_crypto_data(crypto_name):
    # Define the base URL and format the URL for the specific cryptocurrency
    base_url = 'https://coinmarketcap.com/currencies/'
    url = f'{base_url}{crypto_name.lower().replace(" ", "-")}/'

    try:
        # Sending a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Parsing the content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Finding the metrics table
        metrics_table = soup.find('dl', class_='sc-d1ede7e3-0 bwRagp coin-metrics-table')

        if not metrics_table:
            print(f"Error: Unable to find metrics table for {crypto_name}")
            return None

        # Extracting data for Market Cap
        market_cap_label = metrics_table.find(string='Market cap')
        market_cap_value = 'N/A'
        if market_cap_label:
            market_cap_value = market_cap_label.find_next('dd').text.strip()
            market_cap_value = clean_value(market_cap_value)

        # Extracting data for Volume (24h)
        volume_24h_label = metrics_table.find(string='Volume (24h)')
        volume_24h_value = 'N/A'
        if volume_24h_label:
            volume_24h_value = volume_24h_label.find_next('dd').text.strip()
            volume_24h_value = clean_value(volume_24h_value)

        # Extracting data for Volume/Market cap (24h)
        volume_market_cap_label = metrics_table.find(string='Volume/Market cap (24h)')
        volume_market_cap_value = 'N/A'
        if volume_market_cap_label:
            volume_market_cap_value = volume_market_cap_label.find_next('dd').text.strip()

        # Extracting data for Circulating supply
        circulating_supply_label = metrics_table.find(string='Circulating supply')
        circulating_supply_value = 'N/A'
        if circulating_supply_label:
            circulating_supply_value = circulating_supply_label.find_next('dd').text.strip()

        # Extracting data for Total supply
        total_supply_label = metrics_table.find(string='Total supply')
        total_supply_value = 'N/A'
        if total_supply_label:
            total_supply_value = total_supply_label.find_next('dd').text.strip()

        # Extracting data for Max. supply
        max_supply_label = metrics_table.find(string='Max. supply')
        max_supply_value = 'N/A'
        if max_supply_label:
            max_supply_value = max_supply_label.find_next('dd').text.strip()

        if max_supply_value == '\u221e':
            max_supply_value = 'null'
 
        # Extracting data for Fully diluted market cap
        fully_diluted_market_cap_label = metrics_table.find(string='Fully diluted market cap')
        fully_diluted_market_cap_value = 'N/A'
        if fully_diluted_market_cap_label:
            fully_diluted_market_cap_value = fully_diluted_market_cap_label.find_next('dd').text.strip()

        # Creating a dictionary to hold the extracted data
        crypto_data = {
            "Cryptocurrency": crypto_name,
            "Market Cap": market_cap_value,
            "Volume (24h)": volume_24h_value,
            "Volume/Market Cap (24h)": volume_market_cap_value,
            "Circulating Supply": circulating_supply_value,
            "Total Supply": total_supply_value,
            "Max Supply": max_supply_value,
            "Fully Diluted Market Cap": fully_diluted_market_cap_value
        }

        return crypto_data

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching data for {crypto_name}: {e}")
        return None

# Example usage:
crypto_name = 'tether'
bitcoin_data = scrape_crypto_data(crypto_name)
if bitcoin_data:
    print(f"{crypto_name} Data:")
    print(json.dumps(bitcoin_data, indent=4))
else:
    print(f"Failed to retrieve data for {crypto_name}.")
