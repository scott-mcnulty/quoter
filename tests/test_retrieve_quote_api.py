import json
import datetime
import time
import random

import requests

import test_config
import test_utils


def test_retrieve_quote():

    test_utils.store_example_quote(test_utils.EXAMPLE_QUOTE)

    req = requests.get(
        test_config.RETRIEVE_QUOTE_API_URL + '{}'.format(
            test_utils.EXAMPLE_QUOTE.get('id')
        )
    )

    response_json = req.json()
    EXAMPLE_QUOTE = test_utils.EXAMPLE_QUOTE
    assert req.status_code == 200
    assert response_json.get('id') == EXAMPLE_QUOTE.get('id')
    assert response_json.get('title') == EXAMPLE_QUOTE.get('title')
    assert response_json.get('content') == EXAMPLE_QUOTE.get('content')
    assert response_json.get('link') == EXAMPLE_QUOTE.get('link')

    # Since we were converting the custom meta before to plain str we have
    # to reconvert back to a dict
    assert json.loads(
        response_json.get('custom_meta').replace("'", '"')
    ) == EXAMPLE_QUOTE.get('custom_meta')


def test_retrieve_non_existing_quote():

    req = requests.get(
        test_config.RETRIEVE_QUOTE_API_URL + '{}'.format('-1')
    )

    assert req.status_code == 200
    assert req.json() == {}
