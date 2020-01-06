from flask import abort, jsonify
from flask_restful import Resource, reqparse
from marshmallow import ValidationError

from api.db import db_session
from api.models import AuthorTable, BookTable
from api.schemas import AuthorInputSchema, AuthorOutputSchema


class Author(Resource):

    def get(self, id=None):
        pass

    def post(self):
        pass

    def put(self, id=None):
        pass

    def delete(self, id=None):
        pass
