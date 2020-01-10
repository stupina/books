from flask import Flask

from api.db import db, migrate
from api.api import create_api


def create_app(configuration):
    app = Flask(__name__)
    app.config.from_object(configuration)
    db.init_app(app)
    migrate.init_app(app, db)
    create_api(app)
    return app
