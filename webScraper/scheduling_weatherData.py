from config_info.config_info import MySQL, APIkeys
import requests
import json
import traceback
import time
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# use Crontab to execute every 5 mins


def main():
    try:
        url = f'https://api.openweathermap.org/data/2.5/weather?lat=53.332383&lon=-6.252717&appid={APIkeys.weather_APIKEY}'
        response = requests.get(url)
        weather_data = response.json()
        print(weather_data)
        return weather_data

    except:
        # if there is any problem, print the traceback
        print(traceback.format_exc())
    return


main()
