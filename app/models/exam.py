from app.db.database import db
from mongoengine.fields import DateTimeField, ListField


class Result(db.EmbeddedDocument):
    question_id = db.ObjectIdField()
    answer_id = db.IntField(db_field="answer_id")


class StudentAnswer(db.EmbeddedDocument):
    student_id = db.ObjectIdField()
    answers = ListField(db.EmbeddedDocumentField(Result), required=False)
    total_point = db.FloatField()


class Question(db.EmbeddedDocument):
    question_id = db.ObjectIdField()
    question_name = db.StringField(required=True)
    level = db.IntField()
    answer = ListField()
    correct_answer = db.IntField()


class Exam(db.Document):
    exam_id = db.ObjectIdField(db_field="_id")
    exam_name = db.StringField(db_field="exam_name")
    room_id = db.ObjectIdField(db_field="room_id")
    teacher_id = db.ObjectIdField(db_field="teacher_id")
    subject_id = db.ObjectIdField(db_field="subject_id")
    duration = db.IntField(required=True)
    questions = ListField(db.EmbeddedDocumentField(Question))
    students = ListField(
        db.EmbeddedDocumentField(StudentAnswer), required=False
    )
    create_at = DateTimeField()
    expire_at = DateTimeField()
