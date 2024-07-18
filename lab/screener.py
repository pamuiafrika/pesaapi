import requests
from bs4 import BeautifulSoup
import json

# URL of the webpage to scrape
url = "https://www.nasdaq.com/market-activity/stocks/screener"

# Headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "DNT": "1",  # Do Not Track Request Header
    "Upgrade-Insecure-Requests": "1",
}

# Create a session to handle cookies
session = requests.Session()
session.headers.update(headers)

try:
    # Send a GET request to the URL with headers
    response = session.get(url)
    response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
    print("Request was successful.")
    
    # Check the content of the response
    if response.text:
        print("Response content is not empty.")
    
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Check if the parsing was successful
    if soup:
        print("HTML content parsed successfully.")

    # Find the table with class "nasdaq-screener__table"
    table = soup.find('table', class_='nasdaq-screener__table')
    if table:
        print("Table found.")

        # Extract table headers
        header_row = table.find('thead').find('tr')
        headers = [header.text.strip() for header in header_row.find_all('th')]
        if headers:
            print("Headers extracted:", headers)
        else:
            print("No headers found.")
        
        # Extract rows of the table
        tbody = table.find('tbody')
        if tbody:
            rows = tbody.find_all('tr')
            print(f"Found {len(rows)} rows.")
            
            # Iterate through rows and extract cell data
            data = []
            for row in rows:
                cells = row.find_all(['th', 'td'])
                if len(cells) == len(headers):
                    cell_data = {headers[i]: cells[i].text.strip() for i in range(len(cells))}
                    data.append(cell_data)
                else:
                    print(f"Skipping row with {len(cells)} cells: {row}")
            
            # Convert the data to JSON format
            json_data = json.dumps(data, indent=4)
            
            # Print the JSON data
            print(json_data)
        else:
            print("No tbody found in the table.")
    else:
        print("Table not found.")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
