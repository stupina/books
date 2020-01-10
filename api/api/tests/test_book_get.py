from operator import attrgetter

from api.tests.base import BaseTestCase
from api.tests.factories import AuthorTableFactory, BookTableFactory


class BookGetTestCase(BaseTestCase):
    def test_empty_db(self):
        response = self.client.get('/books')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_with_one_record(self):
        book = BookTableFactory()
        book_json = [{
            'id': book.id,
            'name': book.name,
            'rating': book.total_rating,
            'authors': [],
        }]

        response = self.client.get('/books/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, book_json)

    def test_get_author_by_id(self):
        book = BookTableFactory()
        book_json = [{
            'id': book.id,
            'name': book.name,
            'rating': book.total_rating,
            'authors': [],
        }]

        uri = f'/books/{book.id}'
        response = self.client.get(uri)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json, book_json)

    def test_author_with_books(self):
        authors = AuthorTableFactory.create_batch(3)
        book = BookTableFactory.create(authors=authors)
        authors = [
            {
                'id': author.id,
                'name': author.name,
            }
            for author in authors
        ]
        book_json = [{
            'id': book.id,
            'name': book.name,
            'authors': authors,
            'rating': book.total_rating,
        }]

        response = self.client.get('/books')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, book_json)

    def test_author_get_without_pagination(self):
        books = BookTableFactory.create_batch(7)
        books_json = [
            {
                'id': book.id,
                'name': book.name,
                'rating': book.total_rating,
                'authors': [],
            }
            for book in books
        ]

        response = self.client.get('/books')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, books_json)

    def test_author_get_with_pagination(self):
        books = BookTableFactory.create_batch(7)
        books_json = [
            {
                'id': book.id,
                'name': book.name,
                'rating': book.total_rating,
                'authors': [],
            }
            for book in books
        ]
        page = 2
        per_page = 3
        start_index = (page-1) * per_page
        stop_index = (page-1) * per_page + per_page

        uri = f'/books?page={page}&per_page={per_page}'
        response = self.client.get(uri)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, books_json[start_index:stop_index])
