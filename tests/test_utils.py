import requests

import test_config


def get_random_quote():

    req = requests.get(test_config.RANDOM_QUOTE_API_URL)
    return req.json()
