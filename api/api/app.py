import os

from flask import Flask

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']


@app.route("/")
def index():
    return "The app has been started"
