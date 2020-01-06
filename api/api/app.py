import os

from flask import Flask
from flask_restful import Api

from api.resources.book import Book
from api.resources.author import Author

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']
app_api = Api(app)


app_api.add_resource(Book, "/books", "/books/", "/books/<int:id>")
app_api.add_resource(Author, "/authors", "/authors/", "/authors/<int:id>")


@app.route("/")
def index():
    return "The app has been started"
