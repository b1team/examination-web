from mongoengine.fields import ListField
from app.db.database import db


class Subject(db.Document):
    subject_id = db.ObjectIdField()
    subject_name = db.StringField()
    teacher_id = db.ObjectIdField(db_field="teacher_id")
