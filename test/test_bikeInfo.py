import unittest
from bikeInfo import functions


class TestBikeInfo(unittest.TestCase):

    def test_get_data(self):
        obj = functions.get_data()
        print(obj[0])

    def test_check_connection(self):
        functions.check_connection()

    def test_init_database(self):
        functions.init_database()

    def test_store_station(self):
        functions.store_station()

    def test_store_availability(self):
        functions.store_availability()
