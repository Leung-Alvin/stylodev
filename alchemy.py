from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.sql import text
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Corpus():
    __tablename__ = 'corpus'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column()
    author: Mapped[str] = mapped_column()

    def __init__(self, text, author):
        self.text = text
        self.author = author


if __name__ == '__main__':
    engine = create_engine('postgresql://postgres:aleung@localhost/test')
    if not database_exists(engine.url):
        create_database(engine.url)