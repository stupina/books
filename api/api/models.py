from api.db import db
from sqlalchemy.ext.hybrid import hybrid_property


authors_books_rel = db.Table(
    'authors_books',
    db.Column(
        'author_id',
        db.Integer,
        db.ForeignKey('author.id', ondelete='SET NULL'),
        primary_key=True,
    ),
    db.Column(
        'book_id',
        db.Integer,
        db.ForeignKey('book.id', ondelete='SET NULL'),
        primary_key=True,
    ),
)


class BookTable(db.Model):
    __tablename__ = 'book'
    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    name = db.Column(
        db.String(60),
        unique=True,
    )
    authors = db.relationship(
        'AuthorTable',
        secondary=authors_books_rel,
        back_populates='books',
    )
    number_of_ratings = db.Column(
        db.Integer,
        default=0,
    )
    total_rating = db.Column(
        db.Float,
        default=0,
    )


class AuthorTable(db.Model):
    __tablename__ = 'author'
    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    name = db.Column(
        db.String(60),
        unique=True,
    )
    books = db.relationship(
        'BookTable',
        secondary=authors_books_rel,
        back_populates='authors',
        order_by='desc(BookTable.total_rating)',
    )

    @hybrid_property
    def top_5_books(self):
        return self.books[:5]
