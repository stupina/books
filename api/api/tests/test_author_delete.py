from api.tests.base import BaseTestCase
from api.models import AuthorTable
from api.tests.factories import AuthorTableFactory


class AuthorDeleteTestCase(BaseTestCase):

    def test_author_delete(self):
        author_id = 1
        author = AuthorTableFactory(id=author_id)

        response = self.client.delete(f'authors/{author_id}')
        author = AuthorTable.query.filter_by(id=author_id).first()

        self.assertEqual(response.status_code, 204)
        self.assertFalse(author)

    def test_author_delete_response_without_id(self):
        author = AuthorTableFactory()

        response = self.client.delete('/authors')

        self.assertEqual(response.status_code, 400)

    def test_author_delete_response_with_wrong_id(self):
        author_id = 1
        wrong_id = 2
        author = AuthorTableFactory(id=author_id)

        response = self.client.delete(f'authors/{wrong_id}')

        self.assertEqual(response.status_code, 400)
