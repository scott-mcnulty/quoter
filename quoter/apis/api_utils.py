import json
import logging

import falcon

import logging_config

logger = logging.getLogger(logging_config.LOGGER_NAME)


def check_for_json_body(req, required_fields):
    """
    Checks request, req, for a json body.
    Raise falcon.errors.HTTPMissingParam if no body.
    """

    body = req.stream.read()
    json_data = {}
    if body:
        json_data = json.loads(body)
        logging.info('Request had json body: {}'.format(json_data))

    else:
        logging.error('Request had no json body')
        raise falcon.errors.HTTPMissingParam(
            required_fields
        )

    return json_data


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
