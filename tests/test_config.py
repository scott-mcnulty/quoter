import os

PORT = os.environ.get('PORT', 8000)
BASE_URL = "http://localhost:{}".format(PORT)

API_URL = "{}/api".format(BASE_URL)
QUOTE_API_URL = "{}/quote".format(API_URL)
QUOTE_RANDOM_API_URL = "{}/random".format(QUOTE_API_URL)
QUOTE_CREATOR_API_URL = "{}/create".format(QUOTE_RANDOM_API_URL)
QUOTE_RETRIEVER_API_URL = "{}/retrieve".format(QUOTE_RANDOM_API_URL)
