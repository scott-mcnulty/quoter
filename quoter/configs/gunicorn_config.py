import os
import sys


bind = ':{}'.format(os.environ.get('PORT', 8000))
workers = int(os.environ.get('GUNICORN_PROCESSES', '1'))
threads = int(os.environ.get('GUNICORN_THREADS', '1'))
