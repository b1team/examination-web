from flask import Flask
from app.db.database import initialize_db


from app.routers.user import student, teacher
def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('settings.py')

    initialize_db(app)



    app.register_blueprint(student.user)
    app.register_blueprint(teacher.user)

    return app
