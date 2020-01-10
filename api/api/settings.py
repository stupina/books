import os


class Configuration:
    APP_SECRET_KEY = os.getenv('APP_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgres://%s:%s@%s:%s/%s' % (
        os.getenv('POSTGRES_USER'),
        os.getenv('POSTGRES_PASSWORD'),
        'db',
        '5432',
        os.getenv('POSTGRES_DB'),
    )


class TestConfiguration:
    APP_SECRET_KEY = 'test_app_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
    LIVESERVER_PORT = 0
