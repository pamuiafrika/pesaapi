import requests
from bs4 import BeautifulSoup
import json

# URL of the page to scrape
url = "https://finance.yahoo.com/quote/TSLA/"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the regular market price
    regular_market_price_elem = soup.find('fin-streamer', {'data-testid': 'qsp-price'})
    regular_market_price = regular_market_price_elem.find('span').text if regular_market_price_elem else None

    # Extract the regular market price change
    regular_market_change_elem = soup.find('fin-streamer', {'data-testid': 'qsp-price-change'})
    regular_market_change = regular_market_change_elem.find('span').text if regular_market_change_elem else None

    # Extract the regular market price change percent
    regular_market_change_percent_elem = soup.find('fin-streamer', {'data-testid': 'qsp-price-change-percent'})
    regular_market_change_percent = regular_market_change_percent_elem.find(
        'span').text if regular_market_change_percent_elem else None

    # Extract the post-market price
    post_market_price_elem = soup.find('fin-streamer', {'data-testid': 'qsp-post-price'})
    post_market_price = post_market_price_elem.find('span').text if post_market_price_elem else None

    # Extract the post-market price change
    post_market_change_elem = soup.find('fin-streamer', {'data-testid': 'qsp-post-price-change'})
    post_market_change = post_market_change_elem.find('span').text if post_market_change_elem else None

    # Extract the post-market price change percent
    post_market_change_percent_elem = soup.find('fin-streamer', {'data-testid': 'qsp-post-price-change-percent'})
    post_market_change_percent = post_market_change_percent_elem.find(
        'span').text if post_market_change_percent_elem else None

    # Extract market time notices
    market_time_notice_elem = soup.find('div', {'slot': 'marketTimeNotice'})
    market_time_notice = market_time_notice_elem.find('span').text if market_time_notice_elem else None

    # Check if there are enough elements found for after-hours notice
    after_hours_notice_elem = soup.find_all('div', {'slot': 'marketTimeNotice'})
    after_hours_notice = None
    if len(after_hours_notice_elem) > 1:
        after_hours_notice = after_hours_notice_elem[1].find('span').text

    # Create a dictionary with the extracted information
    data = {
        "regular_market_price": regular_market_price,
        "regular_market_change": regular_market_change,
        "regular_market_change_percent": regular_market_change_percent,
        "post_market_price": post_market_price,
        "post_market_change": post_market_change,
        "post_market_change_percent": post_market_change_percent,
        "market_time_notice": market_time_notice,
        "after_hours_notice": after_hours_notice
    }

    # Convert the dictionary to a JSON string
    json_data = json.dumps(data, indent=4)

    # Print the JSON data
    print(json_data)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
