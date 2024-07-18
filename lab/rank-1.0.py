import requests
from bs4 import BeautifulSoup

# URL of the website to scrape
url = 'https://coinmarketcap.com/'

# Send a GET request to the URL
response = requests.get(url)
html_content = response.text

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find the table containing the cryptocurrency data
table = soup.find('table', class_='cmc-table')

# Check if the table is found
if table:
    # Find all rows in the table body
    rows = table.find('tbody').find_all('tr')

    # Loop through each row to extract data
    for row in rows:
        # Extract specific data from each row
        rank_element = row.find('td', class_='cmc-table__cell--rank')
        name_element = row.find('p', class_='sc-1eb5slv-0 gGIpIK')
        price_element = row.find('td', class_='cmc-table__cell--sort-by__price')

        if rank_element and name_element and price_element:
            # Extract text from nested <a> tag within price_element
            price_a_tag = price_element.find('a')
            if price_a_tag:
                price = price_a_tag.text.strip()
            else:
                price = price_element.text.strip()
            
            rank = rank_element.text.strip()
            name = name_element.text.strip()
            
            print(f"Rank: {rank}, Name: {name}, Price: {price}")
        else:
            print("Incomplete data for this row.")
else:
    print('Table not found.')
