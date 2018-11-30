"""
Models for the different tables we'll be using.
"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Quote(Base):
    """
    Table to store quotes.
    """
    __tablename__ = 'quotes'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=False)
    title = Column(String(50), nullable=False)
    content = Column(String(1000), nullable=False)
    link = Column(String(100), nullable=False)
    custom_meta = Column(String(250), nullable=True)

    def __repr__(self):
        return (
            '<Quote(id={}, '
            'title={}, '
            'content={}, '
            'link={}, '
            'custom_meta={})>'.format(
                self.id,
                self.title,
                self.content,
                self.link,
                self.custom_meta
            )
        )

    def dictionary_representation(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'link': self.link,
            'custom_meta': self.custom_meta
        }
