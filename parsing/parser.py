import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import time

url = 'https://surnames.behindthename.com/names/usage/english/'

# Path to current script directory
script_directory = os.path.dirname(os.path.abspath(__file__))

# Path to data dir
data_directory = os.path.join(os.path.dirname(script_directory), "data")

# Path to webdriver
driver_path = os.path.join(script_directory, "msedgedriver.exe")

# Create objects Service & Options
service = Service(driver_path)
options = Options()

# Add arguments for Options
# options.add_argument('--page-load-strategy=interactive')  
# options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-browser-side-navigation')
options.add_argument('--disable-infobars')
options.add_argument('--disable-notifications')
options.add_argument('--disable-default-apps')
options.add_argument('--disable-web-security')
options.add_argument('--disable-logging')
options.add_argument('--no-sandbox')
# # options.add_argument('--headless')
options.add_argument('--remote-debugging-port=9222')
options.add_argument('--disable-bundled-ppapi-flash')
options.add_argument('--blink-settings=imagesEnabled=false')
options.add_argument("--blink-settings=imagesEnabled=false")
prefs = {
    'profile.managed_default_content_settings.fonts': 1  
}
options.add_experimental_option('prefs', prefs)


# M Edge browser init 
driver = webdriver.Edge(service=service, options=options)

driver.get(url)
time.sleep(4)



soup = BeautifulSoup(driver.page_source, 'html.parser')
surnames_array = []
# Search for all blocks with class 'browsename' and extract the names
name_blocks = soup.find_all('div', class_='browsename')
for name_block in name_blocks:
    name = name_block.find('span', class_='listname').text.strip()
    result_string = ''.join(char for char in name if not char.isdigit())
    surnames_array.append(result_string)

for i in range(2, 7, 1):
    current_url = url+str(i)
    driver.get(current_url)
    time.sleep(4)
    # Use BeautifulSoup to parse the HTML code of the current page
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Search for all blocks with class 'browsename' and extract the names
    name_blocks = soup.find_all('div', class_='browsename')
    for name_block in name_blocks:
        name = name_block.find('span', class_='listname').text.strip()
        result_string = ''.join(char for char in name if not char.isdigit())
        surnames_array.append(result_string)

url = 'https://www.behindthename.com/names/usage/american/'
driver.get(url)
time.sleep(4)
soup = BeautifulSoup(driver.page_source, 'html.parser')
names_array = []
# Search for all blocks with class 'browsename' and extract the names
name_blocks = soup.find_all('div', class_='browsename')
for name_block in name_blocks:
    name = name_block.find('span', class_='listname').text.strip()
    result_string = ''.join(char for char in name if not char.isdigit())
    names_array.append(result_string)

for i in range(2, 16, 1):
    current_url = url+str(i)
    driver.get(current_url)
    time.sleep(4)
    # Use BeautifulSoup to parse the HTML code of the current page
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    name_blocks = soup.find_all('div', class_='browsename')
    for name_block in name_blocks:
        name = name_block.find('span', class_='listname').text.strip()
        result_string = ''.join(char for char in name if not char.isdigit())
        names_array.append(result_string)
driver.quit()

file_name = "name.txt"
# Open the file for writing
with open(data_directory+"\\" +file_name, 'w', encoding='utf-8') as file:
    # Write each element of the array line by line
    for item in names_array:
        file.write(f"{item}\n")

file_name = "surname.txt"
# Open the file for writing
with open(data_directory+"\\" +file_name, 'w') as file:
    # Write each element of the array line by line
    for item in surnames_array:
        file.write(f"{item}\n")
