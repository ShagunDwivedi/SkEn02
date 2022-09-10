import json
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup

import pandas as pd
import re

from datetime import datetime

required_city = input("Enter City Name: ")
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

high_temp_daily_list = [high_temp_daily[i].text.strip().split()[0] for i in range(len(high_temp_daily))]
low_temp_daily_list = [low_temp_daily[i].text.strip().split()[0] for i in range(len(low_temp_daily))]
summ_daily_list = re.findall('[a-zA-Z][^A-Z]*', summ_daily.text)

#for making a pandas dataframe
datelist = pd.date_range(datetime.today(), periods=len(high_temp_daily)).tolist()

datelist = [datelist[i].date().strftime('%y-%m-%d') for i in range(len(datelist))]
zipping = zip(datelist, high_temp_daily_list, low_temp_daily_list, summ_daily_list)


df = pd.DataFrame(list(zipping), columns=['Date', 'Highest', 'Lowest', 'Summary'])
#print(df.describe())

loc = soup.find('h1', attrs={'id': 'wr-location-name-id'})

#to create a csv_file
#csv_filename = loc.text.split()[0]+'.csv'
#df.to_csv(csv_filename, index=None)

#to create xlsx_file
#xlsx_filename = loc.text.split()[0]+".xlsx"
#df.to_excel(xlsx_filename)

print(required_city, " Today")
print("Highest Temperature: ",high_temp_daily_list[0])
print("Lowest Temperature: ", low_temp_daily_list[0])
print("Summary: ", summ_daily_list[0])
#print(loc.text.split("- ")[1])