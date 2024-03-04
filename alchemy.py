from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy.sql import text
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import sqlalchemy
import os
import unittest

#redacted.txt should contain the following:
#username:password@localhost:5432


def initialize():
    val = input('Enter your postgres login info (username:password): ') + '@localhost:5432'
    metadata_obj = MetaData()

    users = Table(
        'users', 
        metadata_obj,
        Column('id', Integer, primary_key=True),
        Column('username', String),
        Column('password', String),
        Column('email', String),
        Column('date', sqlalchemy.DateTime)
    )

    corpus = Table(
        'corpus', 
        metadata_obj,
        Column('id', Integer, primary_key=True),
        Column("user_id", Integer, ForeignKey("users.id")),
        Column('title', String),
        Column('text', String),
        Column('length', Integer),
        Column('author', String),
        Column('sentiment', String),
        Column('date', sqlalchemy.DateTime)  
    )

    engine = create_engine('postgresql://'+val+'/prints')

    if not database_exists(engine.url):
        create_database(engine.url)

    metadata_obj.create_all(engine)
    print('Database initialized')


# class TestDatabase(unittest.TestCase):
#     val = input('Enter your postgres login info (username:password): ') + '@localhost:5432'
#     def test_prints_engine_exists(self, input=val):
#         concat = 'postgresql://' + input + '/prints'
#         engine = create_engine(concat)
#         self.assertTrue(database_exists(engine.url))
#     def test_connection(self, input=val):
#         concat = 'postgresql://' + input + '/prints'
#         engine = create_engine(concat)
#         conn = engine.connect()
#         self.assertTrue(conn.closed == False)


if __name__ == '__main__':
    # unittest.main()
    initialize()