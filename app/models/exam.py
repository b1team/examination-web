from app.db.database import db
from mongoengine.fields import ListField


class StudentAnswer(db.EmbeddedDocument):
    student_id = db.ObjectIdField()
    question_id = db.ObjectIdField()
    answer_id = db.ObjectIdField()


class Exam(db.Document):
    exam_id = db.ObjectIdField(db_field="_id")
    room_id = db.ObjectIdField(db_field="room_id")
    durantion = db.StringField()
    student_answer = ListField(db.EmbeddedDocumentField(StudentAnswer))
    total_point = db.FloatField()
