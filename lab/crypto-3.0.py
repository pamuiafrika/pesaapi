import requests
from bs4 import BeautifulSoup
import json
import re

def clean_value(value):
    cleaned_value = re.sub(r'^[\d.]+%', '', value).strip()
    return cleaned_value

def clean_coin_name(coin_name):
    cleaned_name = coin_name.split(" price\u00a0")[0].strip()
    return cleaned_name

def clean_price_change(value):
    # Remove trailing "\u00a0(1d)" and keep the percentage change
    cleaned_value = re.sub(r'\s*\(\d+d\)$', '', value).strip()
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

        # Finding the coin stats section
        coin_stats_section = soup.find("div", {"data-module-name": "Coin-stats"})

        # Extracting specific data from the coin stats section
        coin_name = coin_stats_section.find("h1", {"class": "sc-d1ede7e3-0 jPUpok"}).text.strip()
        coin_name = clean_coin_name(coin_name)
        coin_symbol = coin_stats_section.find("span", {"class": "sc-d1ede7e3-0 JCasd base-text"}).text.strip()
        current_price = coin_stats_section.find("span", {"class": "sc-d1ede7e3-0 fsQm base-text"}).text.strip()
        price_change_percent = coin_stats_section.find("p", {"class": "sc-71024e3e-0 sc-58c82cf9-1 ihXFUo iPawMI"}).text.strip()
        price_change_percent = clean_price_change(price_change_percent)
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
            "Coin Name": coin_name,
            "Symbol": coin_symbol,
            "Current Price": current_price,
            "Price Change (1d)": price_change_percent,
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
crypto_name = 'Tether'
bitcoin_data = scrape_crypto_data(crypto_name)
if bitcoin_data:
    print(f"{crypto_name} Data:")
    print(json.dumps(bitcoin_data, indent=4))
else:
    print(f"Failed to retrieve data for {crypto_name}.")
