import json
import logging

import falcon
import sqlalchemy

from apis import api_utils
from utils import log
import database


class StoreQuoteDispatcher:
    """
    Dispatches requests to database wrapper to store quotes.
    """

    # Checked against supplied json for POST and PUT requests
    required_quote_fields = [
        'id',
        'title',
        'content',
        'link'
    ]

    def __init__(self, db):
        self.db = db

    @falcon.before(api_utils.check_for_json_body)
    def on_post(self, req, resp):
        """
        On POST create a new quote record with id in storage
        """

        body = req.media
        if body.get('custom_meta'):
            body['custom_meta'] = str(body['custom_meta'])

        self.db.add_quote(body)
        log('Created quote with values: {}'.format(body))
        response_message = 'Success storing quote: {}'.format(body)
        resp.media = {'message': response_message}

    @falcon.before(api_utils.check_for_json_body)
    def on_put(self, req, resp):
        """
        On PUT update the specified quote record with id from storage
        """

        body = req.media
        if body.get('custom_meta'):
            body['custom_meta'] = str(body['custom_meta'])

        self.db.update_quote(body)
        log('Updated quote with values: {}'.format(body))
        response_message = 'Success updateding quote: {}'.format(body)
        resp.media = {'message': response_message}

    @falcon.before(api_utils.check_for_json_body)
    def on_delete(self, req, resp):
        """
        On DELETE remove the specefied quote record with id from storage
        """

        body = req.media
        self.db.delete_quote(body)
        log('Deleted quote with id: {}'.format(body.get('id')))
        response_message = 'Success deleting quote: {}'.format(body)
        resp.media = {'message': response_message}
