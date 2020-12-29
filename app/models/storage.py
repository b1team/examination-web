from mongoengine.fields import ListField
from app.db.database import db


class Answer(db.EmbeddedDocument):
    id = db.IntField(db_field="id")
    value = db.StringField(required=True)


class Storage(db.Document):
    Id = db.ObjectIdField(db_field="_id")
    teacher_id = db.ObjectIdField(db_field="teacher_id")
    question = db.StringField(required=True)
    answer = ListField(db.EmbeddedDocumentField(Answer))
    correct_answer = db.IntField(required=True)
    level = db.IntField(required=True)
