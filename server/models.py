from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, ForeignKey, String
from sqlalchemy.orm import sessionmaker

import os

# Database connection
_DATABASE = 'sqlite:///db.sqlite3'
_DEBUG = False

# ORM base
_Base = declarative_base()

class Users(_Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    token = Column(String)

class Images(_Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    elo = Column(Integer, nullable=False, default=1000)

class Matches(_Base):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey(Users.id), nullable=False)
    winner = Column(Integer, ForeignKey(Images.id), nullable=False)
    loser = Column(Integer, ForeignKey(Images.id), nullable=False)

# Connect to database
_engine = create_engine(_DATABASE, echo=_DEBUG, convert_unicode=True)
_session_factory = sessionmaker(bind=_engine)
Session = _session_factory()

# Initialize database if it doesn't exist
if not os.path.exists('db.sqlite3'):
    _Base.metadata.create_all(_engine)

    with open('list') as f:
        ids = [int(line[:-5]) for line in f if line]
    Session.bulk_save_objects(Images(id=id) for id in set(ids))
    Session.commit()
