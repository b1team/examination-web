from mongoengine.fields import ListField
from app.db.database import db


class Teacher(db.EmbeddedDocument):
    teacher_id = db.ObjectIdField(required=True)
    teacher_name = db.StringField(required=True)


class Student(db.EmbeddedDocument):
    student_id = db.ObjectIdField(required=True)
    student_name = db.StringField(required=True)


class TeacherSubject(db.EmbeddedDocument):
    subject_id = db.ObjectIdField()
    subject_name = db.StringField()


class Room(db.Document):
    room_id = db.ObjectIdField(db_field="_id")
    room_name = db.StringField(required=True)
    teacher = db.EmbeddedDocumentField(Teacher)
    subject = db.EmbeddedDocumentField(TeacherSubject)
    room_code = db.StringField(required=True)
    student = ListField(db.EmbeddedDocumentField(Student))
