import json
import logging

import falcon
import sqlalchemy

from apis import api_utils
import error_handlers


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

        logging.debug("POST request to creator api.")

        body = req.media
        if body.get('custom_meta'):
            body['custom_meta'] = str(body['custom_meta'])

        try:
            self.db.add_quote(body)
            response_message = 'Success storing quote: {}'.format(body)
            resp.media = {'message': response_message}
            logging.info('Created quote with values: {}'.format(body))

        except sqlalchemy.exc.IntegrityError as ie:
            self.db.rollback()
            logging.error('Database error: {}'.format(ie))
            raise error_handlers.StorageError(falcon.HTTP_500)

    @falcon.before(api_utils.check_for_json_body)
    def on_put(self, req, resp):
        """
        On PUT update the specified quote record with id from storage
        """

        logging.debug("PUT request to creator api.")

        body = req.media
        if body.get('custom_meta'):
            body['custom_meta'] = str(body['custom_meta'])

        try:
            self.db.update_quote(body)
            response_message = 'Success updateding quote: {}'.format(body)
            resp.media = {'message': response_message}
            logging.info('Updated quote with values: {}'.format(body))

        except sqlalchemy.exc.IntegrityError as ie:
            self.db.rollback()
            logging.error('Database error: {}'.format(ie))
            raise error_handlers.StorageError(falcon.HTTP_500)

    @falcon.before(api_utils.check_for_json_body)
    def on_delete(self, req, resp):
        """
        On DELETE remove the specefied quote record with id from storage
        """

        logging.debug("DELETE request to creator api.")

        body = req.media
        try:
            self.db.delete_quote(body)
            response_message = 'Success deleting quote: {}'.format(body)
            resp.media = {'message': response_message}
            logging.info(
                'Deleted quote with id: {}'.format(body.get('id'))
            )

        except sqlalchemy.exc.IntegrityError as ie:
            self.db.rollback()
            logging.error('Database error: {}'.format(ie))
            raise error_handlers.StorageError(falcon.HTTP_500)
