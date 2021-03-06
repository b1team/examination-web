from flask import Flask
from app.db.database import initialize_db
from app.routers.auth import login, register
from app.routers import home, room, exam, error
from app.routers.user import student, teacher, admin


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile("settings.py")
    initialize_db(app)
    app.register_blueprint(home.bp)
    app.register_blueprint(login.auth)
    app.register_blueprint(register.auth)

    app.register_blueprint(home.bp)

    app.register_blueprint(login.auth)
    app.register_blueprint(register.auth)

    app.register_blueprint(student.user)
    app.register_blueprint(teacher.user)
    app.register_blueprint(room.user)
    app.register_blueprint(admin.user)

    app.register_blueprint(exam.user)
    app.register_blueprint(error.user)

    return app
