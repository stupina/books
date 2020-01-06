from flask import abort, jsonify
from flask_restful import Resource, reqparse
from marshmallow import ValidationError

from api.db import db_session
from api.models import AuthorTable, BookTable
from api.schemas import BookInputSchema, BookOutputSchema


class Book(Resource):

    def get(self, id=None):
        if not id:
            books = (db_session.query(BookTable).all())
        else:
            books = ([db_session.query(BookTable).filter_by(id=id).first()])
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
            db_session.add(book)
            db_session.commit()
            message = f'New book with id = {book.id} has been created'
        else:
            book = db_session.query(BookTable).filter_by(id=id).first()
            book.name = name
            book.authors.clear()
            message = f'Book with id = {book.id} has been changed'

        authors = args.get('authors')
        for author_name in authors:
            author = db_session.query(AuthorTable).filter_by(
                name=author_name,
            ).first()
            if not author:
                author = AuthorTable(name=author_name)
            book.authors.append(author)
        db_session.commit()

        status_code = 201
        return message, status_code

    def delete(self, id=None):
        if not id:
            abort(400)
        db_session.query(BookTable).filter_by(id=id).delete()
        db_session.commit()
        message = 'Book has been deleted'
        status_code = 200
        return message, status_code
