from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json
from bs4 import BeautifulSoup

# Path to your ChromeDriver (update this path to the correct one)
webdriver_path = '/home/pamuiafrika/Desktop/Pamui Afrika/incubator/api/PesaAPI/chromedriver'  # Change this to the path to your chromedriver

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass some bot detections
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("start-maximized")  # Open Browser in maximized mode
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Initialize the WebDriver
service = Service(executable_path=webdriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL of the webpage to scrape
url = "https://www.nasdaq.com/market-activity/stocks/screener"
driver.get(url)

# Wait for the page to fully load
time.sleep(5)  # Adjust this time as necessary

# Scroll down to the bottom to ensure dynamic content is loaded
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)  # Give time for any lazy-loaded content to load

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Close the WebDriver
driver.quit()

# Extract data as before
table = soup.find('table', class_='nasdaq-screener__table')
if table:
    headers = [header.text.strip() for header in table.find_all('th')]
    tbody = table.find('tbody')
    if tbody:
        rows = tbody.find_all('tr')
        data = []
        for row in rows:
            cells = row.find_all('td')
            if len(cells) == len(headers):
                cell_data = {headers[i]: cells[i].text.strip() for i in range(len(cells))}
                data.append(cell_data)

        # Convert the data to JSON format
        json_data = json.dumps(data, indent=4)

        # Print the JSON data
        print(json_data)
    else:
        print("No tbody found in the table.")
else:
    print("Table not found.")
