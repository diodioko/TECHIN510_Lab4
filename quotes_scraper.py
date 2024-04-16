import os

import requests
from bs4 import BeautifulSoup


from db import Database

BASE_URL = 'http://quotes.toscrape.com/page/1/'


response = requests.get(URL)
soup = BeautifulSoup(response.text, 'html.parser')
quote_