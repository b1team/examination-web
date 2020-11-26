from flask import Flask
from app.db.database import initialize_db
from app.routers.auth import login, register
from app.routers import home

from app.routers.user import student, teacher


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile("settings.py")

    initialize_db(app)

    app.register_blueprint(home.bp)

    app.register_blueprint(login.auth)
    app.register_blueprint(register.auth)

    app.register_blueprint(student.user)
    app.register_blueprint(teacher.user)

    return app
