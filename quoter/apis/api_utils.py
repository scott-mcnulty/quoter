import json
import logging

import falcon


def check_required_body_fields(json_data, required_fields):
    """
    Checks for our required quote fields in the give jsonbody
    """

    logging.info(
        'Checking json data, {}, against required fields: {}'.format(
            json_data,
            required_fields
        )
    )
    keys = json_data.keys()
    missing_keys = []
    for required_field in required_fields:
        if required_field not in keys:
            logging.error(
                'Request was missing required parameter: {}'.format(
                    required_field
                )
            )
            raise falcon.errors.HTTPMissingParam(required_field)

    return missing_keys


def check_for_json_body(req, resp, params):
    """
    Falcon hook decorator for validating if json was supplied in request.

    https://falcon.readthedocs.io/en/stable/api/hooks.html
    """
    body = req.media
    if not body:
        raise falcon.HTTPBadRequest('Empty request body',
                                    'A valid JSON document is required.')
