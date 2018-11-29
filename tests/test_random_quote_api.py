import json
import datetime
import time
import random

import requests

import test_config


def test_random_quote_api_get():
    req = requests.get(test_config.QUOTE_RANDOM_API_URL)
    assert req.status_code == 200
    assert len(req.json()) == 1


def test_random_quote_api_post():
    req = requests.post(test_config.QUOTE_RANDOM_API_URL)
    assert req.status_code == 200
    assert len(req.json()) == 1


def test_random_quote_api_with_supplied_number_in_body():

    num_quotes = random.randint(1, 5)
    body = {'number': num_quotes}
    req = requests.post(test_config.QUOTE_RANDOM_API_URL, json=body)
    assert req.status_code == 200
    assert len(req.json()) == num_quotes
