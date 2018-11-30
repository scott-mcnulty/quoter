import sys
import logging

import falcon

from database import DatabaseWrapper
import error_handlers
from apis.random_quote import RandomQuote
from apis.retrieve_quote import RetrieveQuoteDispatcher
from apis.store_quote import StoreQuoteDispatcher

from configs import app_config


def register_apis(api):

    api.add_route('/api/quote/{quote_id}', RetrieveQuoteDispatcher(db))
    api.add_route('/api/quote/store', StoreQuoteDispatcher(db))
    api.add_route('/api/quote/random', RandomQuote())
    logging.debug('Apis registered.')

def register_error_handlers(api):
    api.add_error_handler(error_handlers.StorageError, error_handlers.StorageError.handle)

def set_up_logging():
    formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        stream=sys.stdout,
        level=app_config.LOGGING_LEVEL,
        format=formatter)

# Create app
api = falcon.API()
db = DatabaseWrapper()
register_apis(api)
set_up_logging()
