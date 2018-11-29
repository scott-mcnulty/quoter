import os
import sys
import logging


LOGGER_NAME = os.environ.get('LOGGER_NAME', 'quote_logger')
LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE_PATH = './logs/quoter_debug.log'
FORMATTER = logging.Formatter(LOGGING_FORMAT)

# DEBUG level and above logged to file
logging.basicConfig(
    filename=LOG_FILE_PATH,
    filemode='w',
    format=LOGGING_FORMAT,
    level=logging.DEBUG
)

# INFO level and above logged to stdout
STDOUT_STREAM_HANDLER = logging.StreamHandler(sys.stdout)
STDOUT_STREAM_HANDLER.setLevel(logging.INFO)
STDOUT_STREAM_HANDLER.setFormatter(FORMATTER)
