import json
import requests

from weatherInfo.config_info import *


def get_data():
    r = requests.get(WeatherURI)
    # change response json to python object
    return json.loads(r.text)
