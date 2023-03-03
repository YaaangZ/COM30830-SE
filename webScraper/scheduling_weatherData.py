import requests
import traceback
import time
import weather_forcast_data
import logging

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


# I will be using Crontab to execute every 5 mins so there is no need for a while loop

try:
    # this specifies my updates tp the data 
    weather_forcast_data.store_weatherInformation(logger)
    # logger.info(f"Scraper update {number_of_updates} rows.")
    logger.info("Weather information scraped successfully")

except Exception as e:
    # If there is any problem, log the error
    logger.error("An error occurred while scraping weather information")
    logger.error(traceback.format_exc())


