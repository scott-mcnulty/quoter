import json
import logging

import falcon
import sqlalchemy

import apis.api_utils
from utils import log


class RetrieveQuoteDispatcher:
    """
    Dispatches requests to database wrapper to retrieve a quote.
    """

    def __init__(self, db):
        self.db = db

    def get_record(self, id):
        pass

    def on_get(self, req, resp, quote_id):
        """
        On GET request gets the specified record with id from storage
        """
        quote = self.db.get_quote(quote_id)
        if quote:
            log(
                'Got quote with values: {}'.format(
                    quote.dictionary_representation()
                )
            )
            resp.media = quote.dictionary_representation()
        else:
            log('No quote with quote_id: {}'.format(quote_id))
            resp.media = {}


class RetrieveMultipleQuotesDispatcher:
    """
    Dispatches requests to database wrapper to retrieve multiple quotes.
    """

    def __init__(self, db):
        self.db = db

    def get_records(self, quote_ids):
        quotes = self.db.get_quotes(quote_ids)
        log('Got quotes: {}'.format(quotes))
        print(quotes)
        if quotes:
            return [quote.dictionary_representation() for quote in quotes]
        else:
            return {}

    def on_get(self, req, resp):
        """
        On GET request gets the records matching the supplied ids.
        """
        quote_ids = req.params.get('id')
        if type(quote_ids) is not list:
            quote_ids = [quote_ids]

        log(
            'GET request to retrieve stored quotes with ids: {}'.format(
                quote_ids
            )
        )
        resp.media = self.get_records(quote_ids)

    def on_post(self, req, resp, quote_id):
        """
        On POST request uses supplied ids in json body to get records
        from storage.
        """

        body = req.media
        quote_ids = body.get('ids', [])
        logging.info(
            'GET request to retrieve stored quote record with id: {}'.format(
                quote_id
            )
        )
        resp.media = self.get_records(quote_ids)
