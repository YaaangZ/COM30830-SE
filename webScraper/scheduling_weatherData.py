import requests
import json
import traceback
import time
import weather_forcast_data
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from config_info.config_info import MySQL, APIkeys

# use Crontab to execute every 5 mins



try:
    url = f'https://api.openweathermap.org/data/2.5/weather?lat=53.332383&lon=-6.252717&appid={APIkeys.weather_APIKEY}'
    response = requests.get(url)
    weather_data = response.json()
    weather_forcast_data.store_weatherInformation(weather_data)

except:
    # if there is any problem, print the traceback
    print(traceback.format_exc())



