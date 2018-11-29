import time
import logging

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import database_config
import database_models
import logging_config

logger = logging.getLogger(logging_config.LOGGER_NAME)


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
                logger.info('Connected to database.')
                break

            except sqlalchemy.exc.OperationalError as oe:
                logger.error('Could not connect to database on attempt {}. \
                Sleeping then retrying. Error: {}'.format(
                    connection_tries,
                    oe
                ))
                connection_tries += 1
                time.sleep(database_config.RETRY_SLEEP_TIME)

        # Why two ()'s?
        # https://stackoverflow.com/questions/10264150/error-with-sessionmaker
        self.session = sessionmaker(bind=self.engine)()

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
        logger.debug('Created database engine.')

    def create_all_tables(self):
        """
        Creates the mapping of models to database tables
        """

        if not self.engine:
            self.create_engine()
        database_models.Base.metadata.create_all(self.engine)

    def get_quote(self, quote_id):
        """
        Gets a quote using the id in the supplied
        dictionary, args_dict
        """

        logger.debug('Getting quote with id: {}'.format(quote_id))
        quote = self.session.query(database_models.Quote).filter_by(
            id=quote_id).first()
        logger.debug(
            'Got quote: {}'.format(quote.dictionary_representation())
        )
        return quote.dictionary_representation()

    def create_quote(self, args_dict):
        """
        Creates a database_models.Quote object
        from the values in a supplied dictionary, args_dict
        """

        logger.debug(
            'Creating quote object with values: {}'.format(args_dict)
        )
        quote = database_models.Quote(
            id=args_dict.get('id'),
            title=args_dict.get('title'),
            content=args_dict.get('content'),
            link=args_dict.get('link'),
            custom_meta=args_dict.get('custom_meta', 'None')
        )
        logger.debug('Created quote.')
        return quote

    def add_quote(self, args_dict):
        """
        Adds a quote to the database quote table

        args_dict should have fields:
        id, title, content, link, custom_meta
        """

        quote = self.create_quote(args_dict)
        logger.debug('Creating quote record with values: {}'.format(quote))
        try:
            self.session.add(quote)
            self.session.commit()
            logger.debug('Quote record created.')
        except sqlalchemy.exc.InvalidRequestError as ire:
            self.session.rollback()
            logger.error(
                'Could not create quote record. Error: {}'.format(ire)
            )

    def add_quotes(self, args_dict_list):
        """
        Adds many quotes to the database quote table

        args_dict_list is a list of dicts where each
        dict should have fields:
        id, title, content, link, custom_meta
        """

        quotes = [self.create_quote(args_dict) for args_dict in args_dict_list]
        logger.debug('Creating quote records with values: {}'.format(quotes))
        try:
            self.session.add_all(quotes)
            self.session.commit()
            logger.debug('Quote records created.')
        except sqlalchemy.exc.InvalidRequestError as ire:
            self.session.rollback()
            logger.error(
                'Could not create quote records. Error: {}'.format(ire)
            )

    def update_quote(self, args_dict):
        """
        Updates a quote in the database quote table
        based on the quote id

        args_dict should have fields:
        id, title, content, link, custom_meta
        """

        logger.debug(
            'Updating quote with id: {}'.format(args_dict.get('id'))
        )
        quote = self.session.query(database_models.Quote).filter_by(
            id=args_dict.get('id')).first()

        quote.title = args_dict.get('title')
        quote.content = args_dict.get('content')
        quote.link = args_dict.get('link')
        quote.custom_meta = args_dict.get('custom_meta', 'None')
        self.session.commit()
        logger.debug('Updated quote record.')

    def delete_quote(self, args_dict):
        """
        Deletes a quote in the database quote table
        based on the quote id

        args_dict should have fields:
        id
        """

        logger.debug(
            'Deleting quote record with id: {}'.format(args_dict.get('id'))
        )
        quote = self.session.query(database_models.Quote).filter_by(
            id=args_dict.get('id')).first()
        self.session.delete(quote)
        self.session.commit()
        logger.debug('Deleted quote record.')
