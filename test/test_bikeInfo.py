import unittest
from bikeInfo import scraper_for_JCDecaux


class TestBikeInfo(unittest.TestCase):

    def test_get_data(self):
        obj = scraper_for_JCDecaux.get_data()
        print(obj[0])

    def test_check_connection(self):
        scraper_for_JCDecaux.check_connection()

    def test_init_database(self):
        scraper_for_JCDecaux.init_database()

    def test_store_station(self):
        scraper_for_JCDecaux.store_station()

    def test_store_availability(self):
        scraper_for_JCDecaux.store_availability()
