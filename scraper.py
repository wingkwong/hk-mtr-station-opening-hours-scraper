###########################################################
## A python program scraping Hong Kong MTR Stations Opening Hours
###########################################################
## Author: WONG, Wing Kam (@wingkwong)
## License: MIT
## Version: 0.1.0
## Maintainer: @wingkwong
###########################################################

import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

# Defining variables
url = 'http://www.mtr.com.hk/en/customer/services/service_hours_search.php?query_type=search&station=<STATION_ID>'
no_of_stations = 120
df = pd.DataFrame()
df_station_code = []
df_station_id = []
df_chinese_name = []
df_english_name = []
df_open_time = []
df_close_time = []
df_lookup = pd.read_csv('./mtr_lines_and_stations_lookup.csv')

# Fetching html page from MTR Train Services Page
for station_id in range(1, no_of_stations):
    target_url = url.replace('<STATION_ID>', str(station_id))
    req = requests.get(target_url)
    soup = BeautifulSoup(req.content, 'html.parser')
    df_tmp = pd.DataFrame()
    
    if (df_lookup.loc[df_lookup['Station ID'] == station_id].empty) == False:
        filtered_df = df_lookup.loc[df_lookup['Station ID'] == station_id].iloc[0]
        opening_hours = soup.find_all('div', {'class': 'services_content'})[0].find('p').text
        opening_hours = re.findall(r'\s(\d{2}\:\d{2}-\d{2}\:\d{2})', opening_hours)[0].split('-')
        open_time = opening_hours[0]
        close_time = opening_hours [1]
        station_code = filtered_df['Station Code']
        chinese_name = filtered_df['Chinese Name']
        english_name = filtered_df['English Name']
        
        # Add data to tmp arr
        df_station_code.append(station_code)
        df_station_id.append(station_id)
        df_chinese_name.append(chinese_name)
        df_english_name.append(english_name)
        df_open_time.append(open_time)
        df_close_time.append(close_time)

# Add tmp arr to dataframe
df['station_id'] = df_station_id
df['station_code'] = df_station_code
df['chinese_name'] = df_chinese_name
df['english_name'] = df_english_name
df['open_time'] = df_open_time
df['close_time'] = df_close_time

# Writing the result to data folder
df.to_csv('./data/hk-mtr-station-opening-hours.csv', encoding='utf-8', index=False)
