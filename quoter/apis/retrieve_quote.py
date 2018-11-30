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


# class RetrieveMultipleQuotesDispatcher:
#     """
#     Dispatches requests to database wrapper to retrieve multiple quotes.
#     """

#     def __init__(self, db):
#         self.db = db

#     def get_record(self, id):
#         pass

#     def on_get(self, req, resp, quote_id):
#         """
#         On GET request gets the specified record with id from storage
#         """
#         logging.info(
#             'GET request to retrieve stored quote record with id: {}'.format(
#                 quote_id
#             )
#         )
#         quote = self.db.get_quote(quote_id)
#         if quote:
#             resp.media = quote.dictionary_representation()
#         else:
#             resp.media = {}
