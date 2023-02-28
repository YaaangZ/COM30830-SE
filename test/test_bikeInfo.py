import unittest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from webScraper import get_static_data

class TestBikeInfo(unittest.TestCase):

    def test_get_data(self):
        obj = get_static_data.get_dbData()
        print(obj[0])

    def test_check_connection(self):
        get_static_data.check_connection()

    def test_init_database(self):
        get_static_data.create_dbbikes_database()

    def test_store_station(self):
        get_static_data.store_station_information

    def test_store_availability(self):
        get_static_data.store_availability_information()
