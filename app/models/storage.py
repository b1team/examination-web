from mongoengine.fields import ListField
from app.db.database import db


class Answer(db.EmbeddedDocument):
    id = db.IntField(db_field="id")
    value = db.StringField(required=True)


class Storage(db.Document):
    Id = db.ObjectIdField(db_field="_id")
    ques = db.StringField(required=True)
    answ = ListField(db.EmbeddedDocumentField(Answer))
    correct_answer = db.IntField()
    level = db.StringField(required=True)
