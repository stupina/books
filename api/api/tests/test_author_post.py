from api.tests.base import BaseTestCase
from api.models import AuthorTable
from api.tests.factories import AuthorTableFactory


class AuthorPostTestCase(BaseTestCase):

    def test_author_adding_without_books(self):
        data = {
            'name': 'author1',
        }
        response = self.client.post('/authors', data=data)

        self.assertEqual(response.status_code, 400)

    def test_author_adding_with_books(self):
        data = 'name=author1&book=book1&book=book2'
        response = self.client.post(f'/authors?{data}')

        id = int(response.json[0].get('id'))
        author = AuthorTable.query.filter_by(id=id).first()

        self.assertEqual(response.status_code, 201)
        self.assertTrue(author)

    def test_author_change(self):
        author = AuthorTableFactory()
        name = 'Author'
        book_name = 'Book'
        data = f'name={name}&book={book_name}'
        response = self.client.post(f'/authors/{author.id}?{data}')

        id = int(response.json[0].get('id'))
        author = AuthorTable.query.filter_by(id=id).first()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(author.name, name)
        self.assertEqual(author.books[0].name, book_name)
