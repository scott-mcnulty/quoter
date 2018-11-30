import os

PORT = os.environ.get('PORT', 8000)
BASE_URL = "http://localhost:{}".format(PORT)

API_URL = "{}/api".format(BASE_URL)
QUOTE_API_URL = "{}/quote".format(API_URL)
RANDOM_QUOTE_API_URL = "{}/random".format(QUOTE_API_URL)
STORE_QUOTE_API_URL = "{}/store".format(QUOTE_API_URL)
RETRIEVE_QUOTE_API_URL = "{}/".format(QUOTE_API_URL)
