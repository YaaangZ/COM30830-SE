import unittest

from weatherInfo import function


class TestWeatherInfo(unittest.TestCase):

    def test_get_data(self):
        obj = function.get_data()
        print(obj)

    def test_init_database(self):
        function.init_database()

    def test_store_weather_data(self):
        function.store_weather_data()

