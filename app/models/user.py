from app.db.database import db


class User(db.Document):
    user_id = db.ObjectIdField(db_field="_id")
    username = db.StringField(required=True, max_length=15)
    password = db.StringField(required=True)
    email = db.EmailField(required=True)
    gender = db.StringField(required=True)
    classify = db.StringField(required=True)
