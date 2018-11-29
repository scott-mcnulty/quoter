import logging

import falcon

from database import DatabaseWrapper
from apis.random_quote import RandomQuote
from apis.quote_retriever import QuoteRetriever
from apis.quote_creator import QuoteCreator


def register_apis(api):

    api.add_route('/api/quote/{quote_id}', QuoteRetriever(db))
    api.add_route('/api/quote/create', QuoteCreator(db))
    api.add_route('/api/quote/random', RandomQuote())


api = falcon.API()
db = DatabaseWrapper()
register_apis(api)
