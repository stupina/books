from api.tests.base import BaseTestCase
from api.models import BookTable
from api.tests.factories import BookTableFactory


class BookDeleteTestCase(BaseTestCase):

    def test_book_delete(self):
        book_id = 1
        book = BookTableFactory(id=book_id)

        response = self.client.delete(f'books/{book_id}')
        book = BookTable.query.filter_by(id=book_id).first()

        self.assertEqual(response.status_code, 204)
        self.assertFalse(book)

    def test_book_delete_response_without_id(self):
        book = BookTableFactory()

        response = self.client.delete('/books')

        self.assertEqual(response.status_code, 400)

    def test_book_delete_response_with_wrong_id(self):
        book_id = 1
        wrong_id = 2
        book = BookTableFactory(id=book_id)

        response = self.client.delete(f'books/{wrong_id}')

        self.assertEqual(response.status_code, 400)
