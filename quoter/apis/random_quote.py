import mimetypes
import json
import logging

import requests

from configs import app_config


class RandomQuote:

    def get_random(self):
        """
        Gets a random quote from the QUOTE_RESOURCE
        """
        req = requests.get(app_config.RANDOM_QUOTE_URL)
        logging.debug('Got random quote: {}'.format(req.json()))
        return req.json()

    def on_get(self, req, resp):
        """
        Gets a random quote on GET request
        """
        logging.info('GET request for random quote.')
        resp.media = self.get_random()

    def on_post(self, req, resp):
        """
        Gets a random number of quotes based on the supplied parameter
        in the json body, `number`
        """

        # Check if a json body is supplied
        body = req.stream.read()
        json_data = {}
        if body:
            json_data = json.loads(body)

        number = int(json_data.get('number', 1))
        logging.info('GET request for {} random quotes.'.format(number))

        quotes = [self.get_random()[0] for n in range(number)]
        resp.media = quotes
