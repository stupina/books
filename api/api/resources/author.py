from flask import abort, jsonify, make_response
from flask_restful import Resource, reqparse
from marshmallow import ValidationError

from api.db import db
from api.models import AuthorTable, BookTable
from api.schemas import AuthorInputSchema, AuthorOutputSchema, PaginationSchema


class Author(Resource):

    def get(self, id=None):
        author_recs = AuthorTable.query
        if not id:
            try:
                parser = reqparse.RequestParser()
                parser.add_argument('page')
                parser.add_argument('per_page')
                args = parser.parse_args()
                args = PaginationSchema.load(args)
            except ValidationError:
                abort(400)

            page = args.get('page')
            if not page:
                authors = author_recs.all()
            else:
                per_page = args.get('per_page') or 1
                authors = author_recs.paginate(page, per_page).items
        else:
            authors = [author_recs.filter_by(id=id).first()]
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
        except ValidationError:
            abort(400)

        name = args.get('name')
        if not id:
            author = AuthorTable(name=name)
            db.session.add(author)
            db.session.commit()
        else:
            author = AuthorTable.query.filter_by(id=id).first()
            author.name = name
            author.books.clear()

        books = args.get('books')
        for book_name in books:
            book = BookTable.query.filter_by(name=book_name).first()
            if not book:
                book = BookTable(name=book_name)
            author.books.append(book)
        db.session.add(author)
        db.session.commit()

        status_code = 201
        data = jsonify(
            AuthorOutputSchema.dump([author])
        )
        response = make_response(data, status_code)
        return response

    def delete(self, id=None):
        if not id:
            abort(400)
        author = AuthorTable.query.filter_by(id=id).first()
        if not author:
            abort(400)
        db.session.delete(author)
        db.session.commit()
        status_code = 204
        return id, status_code
