import requests
from bs4 import BeautifulSoup

url = "https://coinmarketcap.com/currencies/litecoin/"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find the section containing the coin stats
coin_stats_section = soup.find("div", {"data-module-name": "Coin-stats"})

# Extract specific data from the coin stats section
coin_name = coin_stats_section.find("h1", {"class": "sc-d1ede7e3-0 jPUpok"}).text.strip()
coin_symbol = coin_stats_section.find("span", {"class": "sc-d1ede7e3-0 JCasd base-text"}).text.strip()
current_price = coin_stats_section.find("span", {"class": "sc-d1ede7e3-0 fsQm base-text"}).text.strip()
price_change_percent = coin_stats_section.find("p", {"class": "sc-71024e3e-0 sc-58c82cf9-1 ihXFUo iPawMI"}).text.strip()

# Output the extracted data
print("Coin Name:", coin_name)
print("Symbol:", coin_symbol)
print("Current Price:", current_price)
print("Price Change (1d):", price_change_percent)
