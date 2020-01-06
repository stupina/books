from flask import abort, jsonify
from flask_restful import Resource, reqparse
from marshmallow import ValidationError

from api.db import db_session
from api.models import AuthorTable, BookTable
from api.schemas import BookInputSchema, BookOutputSchema


class Book(Resource):

    def get(self, id=None):
        pass

    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('name')
            parser.add_argument('author', action='append')
            args = parser.parse_args()
            args = BookInputSchema.load(args)
        except ValidationError as err:
            abort(400)

        name = args.get('name')
        book = BookTable(name=name)

        authors = args.get('authors')
        for author_name in authors:
            author = db_session.query(AuthorTable).filter_by(
                name=author_name,
            ).first()
            if not author:
                author = AuthorTable(name=author_name)
            book.authors.append(author)
        db_session.add(book)
        db_session.commit()

        message = f'New book with id = {book.id} has been created'
        status_code = 201
        return message, status_code

    def put(self, id=None):
        pass

    def delete(self, id=None):
        pass
