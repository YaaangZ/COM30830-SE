import requests
import datetime
import json
# from weatherapi_info import *

APIKEY = "86c4b57818061dc4cebb5e6a32d09692"


def scrap_weather(lat, lon):
    url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={APIKEY}'
    response = requests.get(url)

    print(response)


scrap_weather(53.33912505839768, -6.256243642329802)
