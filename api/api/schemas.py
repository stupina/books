from marshmallow import fields, Schema, validate


class BookSchema(Schema):
    id = fields.Int()
    name = fields.Str(
        required=True,
        validate=validate.Length(max=60),
    )
    total_rating = fields.Float(data_key='rating')


class BookInputSchema(Schema):
    name = fields.Str(
        required=True,
        validate=validate.Length(max=60),
    )
    authors = fields.List(
        fields.Str(),
        data_key='author',
        required=True,
    )


class BookOutputSchema(Schema):
    id = fields.Int()
    name = fields.Str(
        required=True,
        validate=validate.Length(max=60),
    )
    total_rating = fields.Float(data_key='rating')
    authors = fields.Nested(
        "AuthorSchema",
        many=True,
        required=True,
    )


BookSchema = BookSchema()
BookInputSchema = BookInputSchema()
BookOutputSchema = BookOutputSchema(many=True)


class AuthorSchema(Schema):
    id = fields.Int()
    name = fields.Str(
        required=True,
        validate=validate.Length(max=60),
    )


class AuthorInputSchema(Schema):
    name = fields.Str(
        required=True,
        validate=validate.Length(max=60),
    )
    books = fields.List(
        fields.Str(),
        data_key='book',
        required=True,
    )


class AuthorOutputSchema(Schema):
    id = fields.Int()
    name = fields.Str(
        required=True,
        validate=validate.Length(max=60),
    )
    top_5_books = fields.Nested(
        "BookSchema",
        many=True,
        required=True,
    )


AuthorSchema = AuthorSchema()
AuthorInputSchema = AuthorInputSchema()
AuthorOutputSchema = AuthorOutputSchema(many=True)


class PaginationSchema(Schema):
    page = fields.Int(
        validate=validate.Range(min=1),
        allow_none=True,
    )
    per_page = fields.Int(
        validate=validate.Range(min=1),
        allow_none=True,
    )


PaginationSchema = PaginationSchema()


class RatingSchema(Schema):
    rating = fields.Int(
        validate=validate.OneOf([1, 2, 3, 4, 5])
    )


RatingSchema = RatingSchema()
