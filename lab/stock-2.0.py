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
    
    # Extract the current price
    current_price_elem = soup.find('div', {'class': 'YMlKec fxKbKc'})
    current_price = current_price_elem.text.strip() if current_price_elem else None
    
    # Extract the percentage change
    percent_change_elem = soup.find('span', {'class': 'V53LMb'})
    percent_change = percent_change_elem.text.strip() if percent_change_elem else None
    
    # Extract the price change today
    price_change_today_elem = soup.find('span', {'class': 'P2Luy Ez2Ioe ZYVHBb'})
    price_change_today = price_change_today_elem.text.strip() if price_change_today_elem else None
    
    # Create a dictionary with the extracted information
    data = {
        "current_price": current_price,
        "percent_change": percent_change,
        "price_change_today": price_change_today
    }
    
    # Convert the dictionary to a JSON string
    json_data = json.dumps(data, indent=4)
    
    # Print the JSON data
    print(json_data)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
