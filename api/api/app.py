import os

from flask import Flask

from api.db import db, migrate
from api.api import create_api
from api.settings import Configuration


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ['APP_SECRET_KEY']
    app.config.from_object(Configuration)
    db.init_app(app)
    migrate.init_app(app, db)
    create_api(app)
    return app
