from api.db import Base
from sqlalchemy import Table, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property


authors_books_rel = Table(
    'authors_books',
    Base.metadata,
    Column('author_id', Integer, ForeignKey('author.id')),
    Column('book_id', Integer, ForeignKey('book.id'))
)


class AuthorTable(Base):
    __tablename__ = 'author'

    id = Column(
        Integer,
        primary_key=True,
    )
    name = Column(
        String(60),
        unique=True,
    )
    books = relationship(
        "BookTable",
        secondary=authors_books_rel,
        back_populates="authors",
    )


class BookTable(Base):
    __tablename__ = 'book'

    id = Column(
        Integer,
        primary_key=True,
    )
    name = Column(
        String(60),
        unique=True,
    )
    authors = relationship(
        "AuthorTable",
        secondary=authors_books_rel,
        back_populates="books",
    )
    rating_sum = Column(
        Integer,
        default=0,
    )
    rating_num = Column(
        Integer,
        default=0,
    )

    @hybrid_property
    def rating(self):
        rating_sum = self.rating_sum
        rating_num = self.rating_num
        if not rating_num:
            result = 0
        else:
            result = rating_sum / rating_num
        return result
