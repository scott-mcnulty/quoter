import requests

import test_config


EXAMPLE_QUOTE = {
        "id": 123,
        "title": "Example quote title",
        "content": "Example quote content",
        "link": "Example quote link",
        "custom_meta": {
            "Source": "Example quote custom_meta.source"
        }
    }


def get_random_quote():

    req = requests.get(test_config.RANDOM_QUOTE_API_URL)
    return req.json()


def store_example_quote(quote_json):
    req = requests.post(test_config.STORE_QUOTE_API_URL, json=quote_json)
