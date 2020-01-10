from operator import attrgetter

from api.tests.base import BaseTestCase
from api.tests.factories import AuthorTableFactory, BookTableFactory


class AuthorGetTestCase(BaseTestCase):
    def test_empty_db(self):
        response = self.client.get('/authors')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_with_one_record(self):
        author = AuthorTableFactory()
        author_json = [{
            'id': author.id,
            'name': author.name,
            'top_5_books': [],
        }]

        response = self.client.get('/authors/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, author_json)

    def test_get_author_by_id(self):
        author = AuthorTableFactory()
        author_json = [{
            'id': author.id,
            'name': author.name,
            'top_5_books': [],
        }]

        uri = f'/authors/{author.id}'
        response = self.client.get(uri)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json, author_json)

    def test_author_top_5_books(self):
        books = BookTableFactory.create_batch(7)
        author = AuthorTableFactory.create(books=books)
        sorted(books, key=attrgetter('total_rating'))
        top_books = [
            {
                'id': book.id,
                'name': book.name,
                'rating': book.total_rating,
            }
            for book in books
        ]
        author_json = [{
            'id': author.id,
            'name': author.name,
            'top_5_books': top_books[:5],
        }]

        response = self.client.get('/authors')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, author_json)

    def test_author_get_without_pagination(self):
        authors = AuthorTableFactory.create_batch(7)
        authors_json = [
            {
                'id': author.id,
                'name': author.name,
                'top_5_books': [],
            }
            for author in authors
        ]

        response = self.client.get('/authors')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, authors_json)

    def test_author_get_with_pagination(self):
        authors = AuthorTableFactory.create_batch(7)
        authors_json = [
            {
                'id': author.id,
                'name': author.name,
                'top_5_books': [],
            }
            for author in authors
        ]
        page = 2
        per_page = 3
        start_index = (page-1) * per_page
        stop_index = (page-1) * per_page + per_page

        uri = f'/authors?page={page}&per_page={per_page}'
        response = self.client.get(uri)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, authors_json[start_index:stop_index])
