from flask_restful import Api
from api.resources.book import Book
from api.resources.author import Author


def create_api(app):
    app_api = Api(app)
    app_api.add_resource(Book, "/books", "/books/", "/books/<int:id>")
    app_api.add_resource(Author, "/authors", "/authors/", "/authors/<int:id>")
