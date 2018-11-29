import json

import falcon


def check_for_json_body(req, required_fields):
    """
    Checks request, req, for a json body.
    Raise falcon.errors.HTTPMissingParam if no body.
    """

    body = req.stream.read()
    json_data = {}
    if body:
        json_data = json.loads(body)

    else:
        raise falcon.errors.HTTPMissingParam(
            required_fields
        )

    return json_data


def check_required_body_fields(json_data, required_fields):
    """
    Checks for our required quote fields in the give jsonbody
    """

    keys = json_data.keys()
    missing_keys = []
    for required_field in required_fields:
        if required_field not in keys:
            raise falcon.errors.HTTPMissingParam(required_field)

    return missing_keys
