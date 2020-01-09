import os


class Configuration:
    SQLALCHEMY_DATABASE_URI = 'postgres://%s:%s@%s:%s/%s' % (
        os.getenv('POSTGRES_USER'),
        os.getenv('POSTGRES_PASSWORD'),
        'db',
        '5432',
        os.getenv('POSTGRES_DB'),
    )
