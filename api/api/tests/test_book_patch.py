from api.tests.base import BaseTestCase
from api.tests.factories import BookTableFactory


class BookPatchTestCase(BaseTestCase):

    def test_book_patch_with_wrong_id(self):
        wrong_id = 1
        response = self.client.patch(f'books/{wrong_id}')

        self.assertEqual(response.status_code, 400)

    def test_book_patch_add_rating(self):
        author_id = 1
        book = BookTableFactory(id=author_id)
        new_rating = 5
        rating = book.total_rating
        rating_num = book.number_of_ratings
        rating_sum = rating * rating_num
        rating_sum += new_rating
        rating_num += 1
        total_rating = rating_sum / rating_num
        data = {'rating': new_rating}

        response = self.client.patch(f'books/{author_id}', data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(book.total_rating, total_rating)
