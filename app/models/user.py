from mongoengine.fields import ListField
from app.db.database import db


class User(db.EmbeddedDocument):
    user_id = db.IntField(db_field="_id")
    username = db.StringField(required=True, max_length=15)
    password = db.StringField(required=True)
    email = db.EmailField(required=True)
    gender = db.StringField(required=True)
    classify = db.StringField(required=True)

class Room(db.Document):
    room_id = db.ObjectIdField(db_field="_id")
    room_name = db.StringField(required=True)
    user_id = db.ObjectIdField(required=True)
    subject = db.StringField(required=True)
    room_code = db.StringField(required=True)


class Answer(db.EmbeddedDocument):
    id = db.IntField(db_field="id")
    value = db.StringField(required=True)


class Storage(db.Document):
    Id = db.ObjectIdField(db_field="_id")
    ques = db.StringField(required=True)
    answ = ListField(db.EmbeddedDocumentField(Answer))
    correct_answer = db.IntField()
    level = db.StringField(required=True)

class Exam(db.Document):
    pass
