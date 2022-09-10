import json
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup

import pandas as pd

from datetime import datetime


def get_city_url(city):
    city = city.lower()
    
    main_url = 'https://city.imd.gov.in/citywx/menu_test.php##'
    response = requests.get(main_url)
    
    soup = BeautifulSoup(response.text, 'html.parser')

    all_states = soup.find_all('a', attrs={'target':'mainframe'})

    for i in all_states:
        #https://city.imd.gov.in/citywx/+

        if(i.text.lower().rstrip(" ")==city):
            #print("https://city.imd.gov.in/citywx/"+i['href'])
            return("https://city.imd.gov.in/citywx/"+i['href'])
    
    for i in all_states:
        #https://city.imd.gov.in/citywx/+

        if(city in i.text.lower().strip()):
            #print("https://city.imd.gov.in/citywx/"+i['href'])
            return("https://city.imd.gov.in/citywx/"+i['href'])
    

city = input("Enter City Name: ")
url = get_city_url(city)
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

#daily highest temperature
table_cells = soup.find_all('td')
#print(table_cells)

datelist=[]
low_temp_daily_list = []
high_temp_daily_list = []
summ_daily = []

for x in range(33,68,5):
    #these numbers are very prone to change 
    #imd is kind of unreliable with this 
    datelist.append(table_cells[x].font.text.strip())
    low_temp_daily_list.append(table_cells[x+1].font.text.strip())
    high_temp_daily_list.append(table_cells[x+2].font.text.strip())
    summ_daily.append(table_cells[x+4].font.text.strip())

#print(datelist, low_temp_daily_list, high_temp_daily_list, summ_daily, sep="\n")

zipping = zip(datelist, high_temp_daily_list, low_temp_daily_list, summ_daily)

df = pd.DataFrame(list(zipping), columns=['Date', 'Highest', 'Lowest', 'Summary'])

#to create a csv_file remove comments from next two lines
#csv_filename = city.lower()+'.csv'
#df.to_csv(csv_filename, index=None)

#to create xlsx_file  remove comments from next two lines
#xlsx_filename = city.lower()+".xlsx"
#df.to_excel(xlsx_filename)

print(city, "Today")
print("Highest Temperature: ",high_temp_daily_list[0])
print("Lowest Temperature: ", low_temp_daily_list[0])
print("Summary: ", summ_daily[0])





