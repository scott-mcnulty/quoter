import time
import logging

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import falcon

from configs import database_config
from utils import log
import database_models


class StorageError(Exception):
    """
    Falcon error handler used for depicting storage errors.
    The error codes are MySQL error codes from:
    https://dev.mysql.com/doc/refman/5.7/en/server-error-reference.html
    """

    @classmethod
    def select_error_to_give(self, error_code):
        """
        Selects error description based on supplied error_code and
        a falcon exception to raise
        """

        if error_code == 1048 or error_code == 1364:
            description = 'Missing required field.'
            falcon_exception = falcon.HTTP_400

        elif error_code == 1062:
            description = (
                'Quote already stored! If you want to update the quote use '
                'a PUT request to /api/create.'
            )
            falcon_exception = falcon.HTTP_409

        else:
            description = 'Some storage error occurred.'
            falcon_exception = falcon.HTTP_500

        return description, falcon_exception

    @staticmethod
    def handle(ex, req, resp, params):
        """
        Handler for the storage errors.
        Rolls back database and picks the message that
        should be sent back based on the MySQL error code.
        The MySQL generated error message doesn't necessarily
        have to be sent back in the response
        """

        error_code, error_message = ex.orig.args
        log(
            'Storage error handler got error `{}`'
            'with code `{}`. Error: {}'.format(
                error_message,
                error_code,
                ex
            ),
            'error'
        )
        db.rollback()
        description, falcon_exception = StorageError.select_error_to_give(
            error_code
        )

        raise falcon.HTTPError(falcon_exception,
                               'Storage Error',
                               description)


class DatabaseWrapper(object):
    """
    Wraps database interaction using sqlalchemy
    """
    engine = None

    def __init__(self):

        connection_tries = 0
        while connection_tries < database_config.NUM_CONNECTION_RETRIES:

            try:
                self.create_all_tables()
                log('Connected to database.')
                break

            except sqlalchemy.exc.OperationalError as oe:
                log(
                    'Could not connect to database on attempt {}. '
                    'Sleeping then retrying. Error: {}'.format(
                        connection_tries,
                        oe
                    ),
                    'error'
                )
                connection_tries += 1
                time.sleep(database_config.RETRY_SLEEP_TIME)

        # Why two ()'s?
        # https://stackoverflow.com/questions/10264150/error-with-sessionmaker
        self.session = sessionmaker(bind=self.engine)()
        self.session.commit()

    def create_engine(self):
        """
        Creates the sqlalchemy engine
        """

        # TODO:
        # Try sqlalchemy.engine_from_config() instead then
        # put config dict in database_config.py
        self.engine = create_engine(
            database_config.CONNECTION_STRING,
            encoding=database_config.DATABASE_ENCODING,
            echo=database_config.ECHO)
        log('Successfully created database engine.')

    def create_all_tables(self):
        """
        Creates the mapping of models to database tables
        """

        if not self.engine:
            self.create_engine()
        database_models.Base.metadata.create_all(self.engine)

    def rollback(self):
        self.session.rollback()

    def get_quote(self, quote_id):
        """
        Gets a quote using the id in the supplied
        dictionary, args_dict
        """

        log('Getting quote with id: {}'.format(quote_id), 'debug')
        quote = self.session.query(database_models.Quote).filter_by(
            id=quote_id).first()
        log('Got quote: {}'.format(quote))

        return quote

    def create_quote(self, args_dict):
        """
        Creates a database_models.Quote object
        from the values in a supplied dictionary, args_dict
        """

        log('Creating quote object with values: {}'.format(args_dict), 'debug')
        quote = database_models.Quote(
            id=args_dict.get('id'),
            title=args_dict.get('title'),
            content=args_dict.get('content'),
            link=args_dict.get('link'),
            custom_meta=args_dict.get('custom_meta', 'None')
        )
        log('Created quote object.', 'debug')
        return quote

    def add_quote(self, args_dict):
        """
        Adds a quote to the database quote table

        args_dict should have fields:
        id, title, content, link, custom_meta
        """

        quote = self.create_quote(args_dict)
        log('Creating quote record with values: {}'.format(quote), 'debug')

        self.session.add(quote)
        self.session.commit()
        log('Created quote record.', 'debug')

    def add_quotes(self, args_dict_list):
        """
        Adds many quotes to the database quote table

        args_dict_list is a list of dicts where each
        dict should have fields:
        id, title, content, link, custom_meta
        """

        quotes = [self.create_quote(args_dict) for args_dict in args_dict_list]
        log('Creating quote records with values: {}'.format(quotes), 'debug')

        self.session.add_all(quotes)
        self.session.commit()
        log('Quote records created.', 'debug')

    def update_quote(self, args_dict):
        """
        Updates a quote in the database quote table
        based on the quote id

        args_dict should have fields:
        id, title, content, link, custom_meta
        """

        log('Updating quote with id: {}'.format(args_dict.get('id'), 'debug'))
        quote = self.session.query(database_models.Quote).filter_by(
            id=args_dict.get('id')).first()

        quote.title = args_dict.get('title')
        quote.content = args_dict.get('content')
        quote.link = args_dict.get('link')
        quote.custom_meta = args_dict.get('custom_meta')
        self.session.commit()
        log('Updated quote record.', 'debug')

    def delete_quote(self, args_dict):
        """
        Deletes a quote in the database quote table
        based on the quote id

        args_dict should have fields:
        id
        """

        log(
            'Deleting quote record with id: {}'.format(args_dict.get('id')),
            'debug'
        )
        quote = self.session.query(database_models.Quote).filter_by(
            id=args_dict.get('id')).first()
        self.session.delete(quote)
        self.session.commit()
        log('Deleted quote record.', 'debug')


# Database wrapper instance
db = DatabaseWrapper()
