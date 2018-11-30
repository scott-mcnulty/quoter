import mimetypes
import json
import logging

import requests

from configs import app_config
from utils import log


class RandomQuote:

    def get_random(self):
        """
        Gets a random quote from the QUOTE_RESOURCE
        """
        req = requests.get(app_config.RANDOM_QUOTE_URL)
        log('Got random quote: {}'.format(req.json()), 'debug')
        return req.json()

    def on_get(self, req, resp):
        """
        Gets a random quote on GET request
        """
        log('GET request for random quote.')
        resp.media = self.get_random()

    def on_post(self, req, resp):
        """
        Gets a random number of quotes based on the supplied parameter
        in the json body, `number`
        """

        body = req.media
        log(
            'POST request for n number of random quotes. '
            'JSON body: {}'.format(body)
        )
        number = int(body.get('number', 1))
        quotes = [self.get_random()[0] for n in range(number)]
        resp.media = quotes
