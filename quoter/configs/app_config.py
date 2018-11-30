import os

QUOTE_RESOURCE = os.environ.get('QUOTE_RESOURCE', 'http://quotesondesign.com')
RANDOM_QUOTE_URL = '{}/wp-json/posts?\
    filter[orderby]=rand&filter[posts_per_page]=1'.format(
        QUOTE_RESOURCE
    )

PORT = os.environ.get('PORT', 8000)
