import json
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup

import pandas
import re

from datetime import datetime

required_city = "Mumbai"
location_url = 'https://locator-service.api.bbci.co.uk/locations?' + urlencode({
   'api_key': 'AGbFAKx58hyjQScCXIYrxuEwJh2W2cmv',
   's': required_city,
   'stack': 'aws',
   'locale': 'en',
   'filter': 'international',
   'place-types': 'settlement,airport,district',
   'order': 'importance',
   'a': 'true',
   'format': 'json'
})

result = requests.get(location_url).json()

url = 'https://www.bbc.com/weather/'+result['response']['results']['results'][0]['id']
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

#daily highest temperature
high_temp_daily = soup.find_all('span', attrs={'class':'wr-day-temperature__high-value'})

#daily lowest temparature
low_temp_daily = soup.find_all('span', attrs={'class': 'wr-day-temperature__low-value'})

#daily summary
summ_daily = soup.find('div', attrs={'class': 'wr-day-summary'})

