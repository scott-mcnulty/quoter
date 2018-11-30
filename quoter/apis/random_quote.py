import mimetypes
import json
import logging

import requests
import grequests

from configs import app_config
from utils import log


class RandomQuote:

    def could_not_get_quote_handler(self, request, exception):
        return {
            'error': 'Could not get random quote from {}'.format(
                app_config.RANDOM_QUOTE_URL
            )
        }

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
        num = int(body.get('number', 1))

        # We want to be nice to the free quote resource we're using so
        # I'm leaving this hard-coded in :)
        if num > 5:
            num = 5

        # Make grequests generator
        rs = (grequests.get(app_config.RANDOM_QUOTE_URL) for n in range(num))

        # Get responses
        reqs = grequests.map(
            rs,
            exception_handler=self.could_not_get_quote_handler
        )

        # Get the json from each requests
        data = [req.json()[0] for req in reqs]
        resp.media = data
