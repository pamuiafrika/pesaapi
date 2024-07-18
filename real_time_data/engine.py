import re
import requests
from bs4 import BeautifulSoup

from .utils import clean_coin_name, clean_price_change, clean_value, clean_volume_value


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

        if coin_stats_section:
            # Extracting specific data from the coin stats section
            coin_name = coin_stats_section.find("h1", {"class": "sc-d1ede7e3-0 jPUpok"})
            if coin_name:
                coin_name = clean_coin_name(coin_name.text.strip())
            else:
                coin_name = 'N/A'

            coin_symbol = coin_stats_section.find("span", {"class": "sc-d1ede7e3-0 JCasd base-text"})
            if coin_symbol:
                coin_symbol = coin_symbol.text.strip()
            else:
                coin_symbol = 'N/A'

            current_price = coin_stats_section.find("span", {"class": "sc-d1ede7e3-0 fsQm base-text"})
            if current_price:
                current_price = current_price.text.strip()
            else:
                current_price = 'N/A'

            price_change_percent = coin_stats_section.find("p", {"class": "sc-71024e3e-0 sc-58c82cf9-1 ihXFUo iPawMI"})
            if price_change_percent:
                price_change_percent = clean_price_change(price_change_percent.text.strip())
            else:
                price_change_percent = 'N/A'
        else:
            print(f"Error: Unable to find coin stats section for {crypto_name}")
            return None

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
            market_cap_value = clean_volume_value(market_cap_value)

        # Extracting data for Volume (24h)
        volume_24h_label = metrics_table.find(string='Volume (24h)')
        volume_24h_value = 'N/A'
        if volume_24h_label:
            volume_24h_value = volume_24h_label.find_next('dd').text.strip()
            volume_24h_value = clean_value(volume_24h_value)
            volume_24h_value = clean_volume_value(volume_24h_value)

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
            "Market Cap": market_cap_value,
            "Volume (24h)": volume_24h_value,
            "Circulating Supply": circulating_supply_value,
            "Total Supply": total_supply_value,
            "Max Supply": max_supply_value,
            "Fully Diluted Market Cap": fully_diluted_market_cap_value
        }
        return crypto_data

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching data for {crypto_name}: {e}")
        return {
            "error": "Error Occured!"
        }


def scrape_stock_data(symbol, market):
    try:
        # Construct the URL based on market and symbol
        url = f"https://www.google.com/finance/quote/{symbol}:{market}?hl=en"

        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response content
            soup = BeautifulSoup(response.content, 'html.parser')

            # Initialize variables to store extracted data
            previous_close = None
            day_range = None
            year_range = None
            market_cap = None
            avg_volume = None
            pe_ratio = None
            dividend_yield = None
            primary_exchange = None
            current_price = None

            # Extract the current price
            current_price_elem = soup.find('div', {'class': 'YMlKec fxKbKc'})
            current_price = current_price_elem.text.strip() if current_price_elem else None

            # Extract all details
            details_divs = soup.find_all('div', {'class': 'gyFHrc'})
            for div in details_divs:
                label = div.find('div', {'class': 'mfs7Fc'})
                value = div.find_next('div', {'class': 'P6K39c'})

                if label and value:
                    label_text = label.text.strip()
                    value_text = value.text.strip()

                    if label_text == "Previous close":
                        previous_close = value_text
                    elif label_text == "Day range":
                        day_range = value_text
                    elif label_text == "Year range":
                        year_range = value_text
                    elif label_text == "Market cap":
                        market_cap = value_text
                    elif label_text == "Avg Volume":
                        avg_volume = value_text
                    elif label_text == "P/E ratio":
                        pe_ratio = value_text
                    elif label_text == "Dividend yield":
                        dividend_yield = value_text
                    elif label_text == "Primary exchange":
                        primary_exchange = value_text

            # Create a dictionary with the extracted information
            data = {
                "symbol": symbol,
                "market": market,
                "current_price": current_price,
                "previous_close": previous_close,
                "day_range": day_range,
                "year_range": year_range,
                "market_cap": market_cap,
                "avg_volume": avg_volume,
                "pe_ratio": pe_ratio,
                "dividend_yield": dividend_yield,
                "primary_exchange": primary_exchange
            }
            return data

        else:
            print(f"Failed to retrieve the page for {symbol}:{market}. Status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching data from {symbol}:{market}: {str(e)}")
        return {
            "error": "Error Occured!"
        }

