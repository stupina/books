from flask import abort, jsonify
from flask_restful import Resource, reqparse
from marshmallow import ValidationError

from api.db import db
from api.models import AuthorTable, BookTable
from api.schemas import (
    BookInputSchema,
    BookOutputSchema,
    PaginationSchema,
    RatingSchema
)


class Book(Resource):

    def get(self, id=None):
        book_recs = BookTable.query
        if not id:
            try:
                parser = reqparse.RequestParser()
                parser.add_argument('page')
                parser.add_argument('per_page')
                args = parser.parse_args()
                args = PaginationSchema.load(args)
            except ValidationError as err:
                abort(400)

            page = args.get('page')
            if not page:
                books = (book_recs.all())
            else:
                per_page = args.get('per_page') or 1
                books = book_recs.paginate(page, per_page, error_out=False)
        else:
            books = ([book_recs.filter_by(id=id).first()])
        result = jsonify(
            BookOutputSchema.dump(books)
        )
        return result

    def post(self, id=None):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('name')
            parser.add_argument('author', action='append')
            args = parser.parse_args()
            args = BookInputSchema.load(args)
        except ValidationError as err:
            abort(400)

        name = args.get('name')
        if not id:
            book = BookTable(name=name)
            db.session.add(book)
            db.session.commit()
            message = f'New book with id = {book.id} has been created'
        else:
            book = BookTable.query.filter_by(id=id).first()
            book.name = name
            book.authors.clear()
            message = f'Book with id = {book.id} has been changed'

        authors = args.get('authors')
        for author_name in authors:
            author = AuthorTable.query.filter_by(
                name=author_name,
            ).first()
            if not author:
                author = AuthorTable(name=author_name)
            book.authors.append(author)
        db.session.commit()

        status_code = 201
        return message, status_code

    def delete(self, id=None):
        if not id:
            abort(400)
        book = BookTable.query.filter_by(id=id).first()
        db.session.delete(book)
        db.session.commit()
        message = 'Book has been deleted'
        status_code = 200
        return message, status_code

    def patch(self, id=None):
        if not id:
            abort(400)

        try:
            parser = reqparse.RequestParser()
            parser.add_argument('rating')
            args = parser.parse_args()
            args = RatingSchema.load(args)
        except ValidationError as err:
            abort(400)

        rating = args.get('rating')
        book = BookTable.query.filter_by(id=id).first()
        total_rating = book.total_rating
        number_of_ratings = book.number_of_ratings
        book.total_rating = (
            (total_rating * number_of_ratings + rating)
            / (number_of_ratings + 1)
        )
        book.number_of_ratings += 1
        db.session.commit()
        message = f'You voted for the book: {rating}'
        status_code = 200
        return message, status_code
