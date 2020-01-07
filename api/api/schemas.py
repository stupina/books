from marshmallow import fields, Schema, validate


class BookSchema(Schema):
    id = fields.Int()
    name = fields.Str(
        required=True,
        validate=validate.Length(max=60),
    )


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
    books = fields.Nested(
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
