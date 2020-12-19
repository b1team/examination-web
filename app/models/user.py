from mongoengine.base.fields import ObjectIdField
from mongoengine.fields import ListField
from app.db.database import db


class User(db.Document):
    username = db.StringField(required=True, max_length=15)
    password = db.StringField(required=True)
    email = db.EmailField(required=True)
    gender = db.StringField(required=True)
    classify = db.StringField(required=True)


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