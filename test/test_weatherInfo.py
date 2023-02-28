import unittest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from  webScraper import weather_forcast_data


class TestWeatherInfo(unittest.TestCase):

    def test_get_data(self):
        obj = weather_forcast_data.get_data()
        print(obj[0])


    def test_check_connection(self):
        weather_forcast_data.check_connection()

    def test_init_database(self):
        weather_forcast_data.create_weather_database()

    def test_store_weatherInformation(self):
        weather_forcast_data.store_weatherInformation()

   
