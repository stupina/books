from flask import abort, jsonify
from flask_restful import Resource, reqparse
from marshmallow import ValidationError

from api.db import db_session
from api.models import AuthorTable, BookTable
from api.schemas import AuthorInputSchema, AuthorOutputSchema


class Author(Resource):

    def get(self, id=None):
        if not id:
            authors = (db_session.query(AuthorTable).all())
        else:
            authors = ([
                db_session.query(AuthorTable).filter_by(id=id).first(),
            ])
        result = jsonify(
            AuthorOutputSchema.dump(authors)
        )
        return result

    def post(self, id=None):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('name')
            parser.add_argument('book', action='append')
            args = parser.parse_args()
            args = AuthorInputSchema.load(args)
        except ValidationError as err:
            abort(400)

        name = args.get('name')
        if not id:
            author = AuthorTable(name=name)
            message = f'New author with id = {author.id} has been created'
        else:
            author = db_session.query(AuthorTable).filter_by(id=id).first()
            author.name = name
            author.books.clear()
            message = f'Author with id = {author.id} has been changed'

        books = args.get('books')
        for book_name in books:
            book = db_session.query(BookTable).filter_by(
                name=book_name,
            ).first()
            if not book:
                book = BookTable(name=book_name)
            author.books.append(book)
        db_session.add(author)
        db_session.commit()

        status_code = 201
        return message, status_code

    def delete(self, id=None):
        if not id:
            abort(400)
        db_session.query(AuthorTable).filter_by(id=id).delete()
        db_session.commit()
        message = 'Author has been deleted'
        status_code = 200
        return message, status_code
