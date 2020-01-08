from api.db import Base
from sqlalchemy import Table, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property


authors_books_rel = Table(
    'authors_books',
    Base.metadata,
    Column(
        'author_id',
        Integer,
        ForeignKey('author.id', ondelete='SET NULL'),
    ),
    Column(
        'book_id',
        Integer,
        ForeignKey('book.id', ondelete='SET NULL'),
    ),
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
        'AuthorTable',
        secondary=authors_books_rel,
        back_populates='books',
    )
    number_of_ratings = Column(
        Integer,
        default=0,
    )
    total_rating = Column(
        Float,
        default=0,
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
        'BookTable',
        secondary=authors_books_rel,
        back_populates='authors',
        order_by='desc(BookTable.total_rating)',
    )

    @hybrid_property
    def top_5_books(self):
        return self.books[:5]
