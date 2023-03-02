import requests
import json
import traceback
import time
import get_static_data
import logging
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from config_info.config_info import MySQL, APIkeys

# using crontab


# Set up the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a file handler and set the log level
file_handler = logging.FileHandler("dbikesscraping.log")
file_handler.setLevel(logging.DEBUG)

# Create a formatter and set it to the file handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"
NAME = "Dublin"

def main():
    while True:
        try:
            # r = requests.get(STATIONS_URI, params={"contract": NAME,
            #                                         "apiKey": APIkeys.Bike_APIKEY})
            # station_info_obj = json.loads(r.text)
            get_static_data.store_availability_information()
            logger.info("Bikes information scraped successfully")
            time.sleep(5 * 60)

        
        except:
            # if there is any problem, print the traceback
            logger.error("An error occurred while scraping dublin bikes information")
            logger.error(traceback.format_exc())


main()