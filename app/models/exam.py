from app.models.room import Student
from app.models.storage import Answer
from app.db.database import db
from mongoengine.fields import ListField


class Answer(db.EmbeddedDocument):
    id = db.IntField(db_field="id")
    value = db.StringField()


class StudentAnswer(db.EmbeddedDocument):
    student_id = db.ObjectIdField()
    student_name = db.StringField()
    answers = ListField(db.EmbeddedDocumentField(Answer))
    total_point = db.FloatField()


class Question(db.EmbeddedDocument):
    question_id = db.ObjectIdField()
    question_name = db.StringField()
    answer = ListField()
    correct_answer = db.IntField()


class Exam(db.Document):
    exam_id = db.ObjectIdField(db_field="_id")
    room_id = db.ObjectIdField(db_field="room_id")
    duration = db.IntField()
    questions = ListField(db.EmbeddedDocumentField(Question))
    students = ListField()
