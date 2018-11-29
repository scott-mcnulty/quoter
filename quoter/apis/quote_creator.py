import json

import falcon
import sqlalchemy

import apis.api_utils as api_utils


class QuoteCreator:
    """
    Creates records in the database
    """

    required_quote_fields = [
        'id',
        'title',
        'content',
        'link'
    ]

    def __init__(self, db):
        self.db = db

    def on_post(self, req, resp):
        """
        On POST create a new quote record with id in storage
        """

        # Check if a json body is supplied
        json_data = api_utils.check_for_json_body(
            req,
            self.required_quote_fields
        )

        # Check for missing required values
        api_utils.check_required_body_fields(
            json_data,
            self.required_quote_fields
        )

        if json_data.get('custom_meta'):
            json_data['custom_meta'] = str(json_data['custom_meta'])

        try:
            self.db.add_quote(json_data)
            response_message = 'Success storing quote: {}'.format(json_data)
            resp.media = {'message': response_message}
        except sqlalchemy.exc.IntegrityError as ie:
            resp.media = {'error': 'Quote already stored!'}

    def on_put(self, req, resp):
        """
        On PUT update the specified quote record with id from storage
        """

        # Check if a json body is supplied
        json_data = api_utils.check_for_json_body(
            req, self.required_quote_fields)

        # Check for missing required values
        api_utils.check_required_body_fields(
            json_data, self.required_quote_fields)

        if json_data.get('custom_meta'):
            json_data['custom_meta'] = str(json_data['custom_meta'])

        try:
            self.db.update_quote(json_data)
            response_message = 'Success updateding quote: {}'.format(json_data)
            resp.media = {'message': response_message}
        except sqlalchemy.exc.IntegrityError as ie:
            resp.media = {'error': 'Could not update quote! {}'.format(ie)}

    def on_delete(self, req, resp):
        """
        On DELETE remove the specefied quote record with id from storage
        """

        # Check if a json body is supplied
        json_data = api_utils.check_for_json_body(
            req,
            self.required_quote_fields
        )

        # Check for missing required values
        api_utils.check_required_body_fields(
            json_data,
            self.required_quote_fields
        )

        try:
            self.db.delete_quote(json_data)
            response_message = 'Success deleting quote: {}'.format(json_data)
            resp.media = {'message': response_message}
        except sqlalchemy.exc.IntegrityError as ie:
            resp.media = {'error': 'Could not delete quote! {}'.format(ie)}
