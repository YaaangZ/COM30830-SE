import requests
import json
import traceback
import time
import weather_forcast_data
import logging
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from config_info.config_info import APIkeys

# Set up the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a file handler and set the log level
file_handler = logging.FileHandler("weatherscraping.log")
file_handler.setLevel(logging.DEBUG)

# Create a formatter and set it to the file handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)


# Use Crontab to execute every 5 mins
try:
    url = f'https://api.openweathermap.org/data/2.5/weather?lat=53.332383&lon=-6.252717&appid={APIkeys.weather_APIKEY}'
    response = requests.get(url)
    weather_data = response.json()
    weather_forcast_data.store_weatherInformation()
    logger.info("Weather information scraped successfully")

except Exception as e:
    # If there is any problem, log the error
    logger.error("An error occurred while scraping weather information")
    logger.error(traceback.format_exc())


