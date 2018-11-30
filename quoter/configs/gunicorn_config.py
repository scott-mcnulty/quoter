# http://docs.gunicorn.org/en/stable/settings.html

import os
import sys

import configs.app_config as app_config


bind = ':{}'.format(os.environ.get('PORT', app_config.PORT))
workers = int(os.environ.get('GUNICORN_PROCESSES', '1'))
threads = int(os.environ.get('GUNICORN_THREADS', '1'))

# http://docs.gunicorn.org/en/stable/settings.html#loglevel
loglevel = os.environ.get('GUNICORN_LOG_LEVEL', 'debug')
