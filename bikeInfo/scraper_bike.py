from functions import store_availability
import logging

# Set up the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a file handler and set its level to DEBUG
file_handler = logging.FileHandler('debug.log')
file_handler.setLevel(logging.DEBUG)

# Create a formatter to format the log messages
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

# Use the logger to log bugs
try:
    store_availability()
except Exception as e:
    logger.exception("An error occurred: %s", e)
