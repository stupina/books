from factory import post_generation, Sequence, SubFactory
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyFloat

from api.db import db
from api.models import AuthorTable, BookTable


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = db.session


class AuthorTableFactory(BaseFactory):
    id = Sequence(lambda n: n)
    name = Sequence(lambda n: f"author_{n}")

    class Meta:
        model = AuthorTable

    @post_generation
    def books(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for book in extracted:
                self.books.append(book)


class BookTableFactory(BaseFactory):
    id = Sequence(lambda n: n)
    name = Sequence(lambda n: f"book_{n}")
    number_of_ratings = Sequence(lambda x: x)
    total_rating = FuzzyFloat(0.0, 1.0)

    class Meta:
        model = BookTable

    @post_generation
    def authors(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for author in extracted:
                self.authors.append(author)
