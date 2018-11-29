import sys
import logging

import falcon

from database import DatabaseWrapper
from apis.random_quote import RandomQuote
from apis.quote_retriever import QuoteRetriever
from apis.quote_creator import QuoteCreator
import app_config
import logging_config


def register_apis(api):

    api.add_route('/api/quote/{quote_id}', QuoteRetriever(db))
    api.add_route('/api/quote/create', QuoteCreator(db))
    api.add_route('/api/quote/random', RandomQuote())
    logger.debug('Apis registered.')

# Set up logging
logger = logging.getLogger(logging_config.LOGGER_NAME)
logger.addHandler(logging_config.STDOUT_STREAM_HANDLER)

# Create app
api = falcon.API()
db = DatabaseWrapper()
register_apis(api)
