from flask import Flask
from app.db.database import initialize_db


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('settings.py')

    initialize_db(app)

    return app
