from flask import abort, jsonify
from flask_restful import Resource, reqparse
from marshmallow import ValidationError

from api.db import db_session
from api.models import AuthorTable, BookTable
from api.schemas import AuthorInputSchema, AuthorOutputSchema, PaginationSchema


class Author(Resource):

    def get(self, id=None):
        author_recs = db_session.query(AuthorTable)
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
                authors = (author_recs.all())
            else:
                per_page = args.get('per_page') or 1
                authors = author_recs.limit(per_page).offset((page-1)*per_page)
        else:
            authors = ([
                author_recs.filter_by(id=id).first(),
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
