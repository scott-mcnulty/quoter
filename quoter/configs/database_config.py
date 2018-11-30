import os

DATABASE_TYPE = os.environ.get('DATABASE_TYPE', 'mysql+pymysql')
DATABASE_USER = os.environ.get('DATABASE_USER', 'user')
DATABASE_USER_PASSWORD = os.environ.get('DATABASE_USER_PASSWORD', 'password')
DATABASE_HOSTNAME = os.environ.get('DATABASE_HOSTNAME', 'localhost')
DATABASE_NAME = os.environ.get('DATABASE_NAME', 'quotes_db')
DATABASE_ENCODING = os.environ.get('DATABASE_ENCODING', 'utf-8')


CONNECTION_STRING = '{}://{}:{}@{}/{}'.format(
    DATABASE_TYPE,
    DATABASE_USER,
    DATABASE_USER_PASSWORD,
    DATABASE_HOSTNAME,
    DATABASE_NAME
)

# https://docs.sqlalchemy.org/en/latest/core/engines.html#sqlalchemy.create_engine.params.echo
ECHO = os.environ.get('DATABASE_ECHO', False)
NUM_CONNECTION_RETRIES = 5
RETRY_SLEEP_TIME = 10
