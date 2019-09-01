import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine

Base = declarative_base()


# User
class User(Base):
    __tablename__ = 'user'

    # column names
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)

    # return as JSON object
    @property
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
        }


# Genre
class Genre(Base):
    __tablename__ = 'genre'

    # column names
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)

    # return as JSON object
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }


# table for movie
class Movie(Base):
    __tablename__ = 'movie'

    # column names
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    genre_id = Column(Integer, ForeignKey('genre.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

    # return as JSON object
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }


engine = create_engine('sqlite:///catalog.db')


Base.metadata.create_all(engine)
