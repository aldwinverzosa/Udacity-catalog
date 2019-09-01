# fill movie catalog db with data
# !/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Genre, Movie, User

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# function add/commit
def add(line):
    session.add(line)
    session.commit()


# Create first user
u = User(email='admin@mywebsite.com')
add(u)

# Create genre
c = Genre(name='Comedy')
add(c)

a = Genre(name='Action')
add(a)

h = Genre(name='Horror')
add(h)

r = Genre(name='Romance')
add(r)

# Add movie to genre
m = Movie(name='Titanic', genre_id=1, user_id=1)
add(m)

m = Movie(name='The Walking Dead', genre_id=1, user_id=1)
add(m)

m = Movie(name='50 Shades', genre_id=1, user_id=1)
add(m)

m = Movie(name='Finding Nemo', genre_id=2, user_id=1)
add(m)

m = Movie(name='Saw', genre_id=3, user_id=1)
add(m)

m = Movie(name='The 100', genre_id=4, user_id=1)
add(m)
