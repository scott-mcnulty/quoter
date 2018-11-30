import sys
import logging

import falcon

import database
from apis.random_quote import RandomQuote
from apis.retrieve_quote import RetrieveQuoteDispatcher
from apis.store_quote import StoreQuoteDispatcher
import sqlalchemy

from configs import app_config


def register_apis(api):

    api.add_route('/api/quote/{quote_id}', RetrieveQuoteDispatcher(db))
    api.add_route('/api/quote/store', StoreQuoteDispatcher(db))
    api.add_route('/api/quote/random', RandomQuote())
    logging.debug('Apis registered.')


def register_error_handlers(api):
    api.add_error_handler(
        sqlalchemy.exc.IntegrityError,
        database.StorageError.handle)


def set_up_logging():
    formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        stream=sys.stdout,
        level=app_config.LOGGING_LEVEL,
        format=formatter)


# Create app, database wrapper instance, and register api addons
api = falcon.API()
db = database.db
register_apis(api)
register_error_handlers(api)
set_up_logging()
