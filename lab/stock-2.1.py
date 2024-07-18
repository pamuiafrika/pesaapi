import requests
from bs4 import BeautifulSoup
import json

# URL of the page to scrape
url = "https://www.google.com/finance/quote/TSLA:NASDAQ?hl=en"

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
    
    # Extract all details
    details_divs = soup.find_all('div', {'class': 'gyFHrc'})
    for div in details_divs:
        label = div.find('div', {'class': 'mfs7Fc'})
        value = div.find('div', {'class': 'P6K39c'})
        
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
            elif label_text == "Avg volume":
                avg_volume = value_text
            elif label_text == "P/E ratio":
                pe_ratio = value_text
            elif label_text == "Dividend yield":
                dividend_yield = value_text
            elif label_text == "Primary exchange":
                primary_exchange = value_text
    
    # Create a dictionary with the extracted information
    data = {
        "previous_close": previous_close,
        "day_range": day_range,
        "year_range": year_range,
        "market_cap": market_cap,
        "avg_volume": avg_volume,
        "pe_ratio": pe_ratio,
        "dividend_yield": dividend_yield,
        "primary_exchange": primary_exchange
    }
    
    # Convert the dictionary to a JSON string
    json_data = json.dumps(data, indent=4)
    
    # Print the JSON data
    print(json_data)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
