import json

import falcon
import sqlalchemy

import apis.api_utils


class QuoteRetriever:
    """
    Retrieves records from the database
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
        resp.media = quote
