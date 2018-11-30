import sys
import logging

import falcon
import sqlalchemy

import database
from apis.random_quote import RandomQuote
from apis.retrieve_quote import RetrieveQuoteDispatcher
from apis.store_quote import StoreQuoteDispatcher
from utils import log
from configs import app_config


def register_apis(api):
    api.add_route(
        '/api/quote/{quote_id}',
        RetrieveQuoteDispatcher(database.db))
    api.add_route('/api/quote/store', StoreQuoteDispatcher(database.db))
    api.add_route('/api/quote/random', RandomQuote())
    log('Apis registered.', 'info')


def register_error_handlers(api):
    api.add_error_handler(
        sqlalchemy.exc.IntegrityError,
        database.StorageError.handle)
    log('Error handlers registered.', 'info')


def register_addons(api):
    register_apis(api)
    register_error_handlers(api)


def create_app():
    api = falcon.API()
    register_addons(api)
    return api
