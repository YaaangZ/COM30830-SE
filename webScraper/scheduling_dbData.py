import requests
import traceback
import time
import get_static_data
import logging



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


try:
    # get_static_data.store_availability_information()
    number_of_updates = get_static_data.store_availability_information(logger)
    logger.info(f"Scraper update {number_of_updates} rows.")
    logger.info("Bikes information scraped successfully")
    
except:
    # if there is any problem, print the traceback
    logger.error("An error occurred while scraping dublin bikes information")
    logger.error(traceback.format_exc())


