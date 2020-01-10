from api.tests.base import BaseTestCase
from api.models import BookTable
from api.tests.factories import BookTableFactory


class BookPostTestCase(BaseTestCase):

    def test_book_adding_without_books(self):
        data = {
            'name': 'book1',
        }
        response = self.client.post('/books', data=data)

        self.assertEqual(response.status_code, 400)

    def test_book_adding_with_books(self):
        data = 'name=book1&author=author1&author=author2'
        response = self.client.post(f'/books?{data}')

        id = int(response.json[0].get('id'))
        book = BookTable.query.filter_by(id=id).first()

        self.assertEqual(response.status_code, 201)
        self.assertTrue(book)

    def test_book_change(self):
        book = BookTableFactory()
        name = 'Book'
        author_name = 'Author'
        data = f'name={name}&author={author_name}'
        response = self.client.post(f'/books/{book.id}?{data}')

        id = int(response.json[0].get('id'))
        book = BookTable.query.filter_by(id=id).first()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(book.name, name)
        self.assertEqual(book.authors[0].name, author_name)
