import logging
import unittest

from ScrapingData.weatherInfo import function
from ScrapingData.weatherInfo.function import store_weather_data


class TestWeatherInfo(unittest.TestCase):

    def test_get_data(self):
        obj = function.get_data()
        print(obj)

    def test_init_database(self):
        function.init_database()

    def test_store_weather_data(self):
        logger = logging.getLogger("test")
        store_weather_data(logger)

