from app.routers.user import (
    user,
    render_template,
    session,
    redirect,
    url_for,
    request,
)
from app.models.exam import Exam, Question
from app.models.storage import Answer, Storage
from app.models.room import Room
from bson import ObjectId


@user.route("/exam-form", methods=["GET"])
def show_exam_form():
    if session.get("user", None):
        if session["user"].get("classify") == "teacher":
            return render_template("createExam.html")
    return redirect(url_for("auth.login"))


@user.route("/exam", methods=["POST"])
def create_exam():
    exam_info = request.form.to_dict()
    if session["user"].get("classify") == "teacher":
        user_id = ObjectId(session["user"].get("user_id"))
        room = Room.objects(teacher__teacher_id=user_id).first()
        storage = Storage.objects()
        questions = []
        for item in storage:
            questions.append(
                Question(
                    question_id=item.Id,
                    question_name=item.question,
                    answer=item.answer,
                    correct_answer=item.correct_answer,
                )
            )
        exam = Exam(
            room_id=room.room_id,
            duration=exam_info.get("duration"),
            questions=questions,
        )
        exam.save()
    return "ok"


@user.route("/exam/<room_id>", methods=["GET"])
def show_exam_question(room_id=None):
    if session.get("user", None):
        if session["user"].get("classify") == "student":
            user_id = ObjectId(session["user"].get("user_id"))
            room = Room.objects(
                **{"student__student_id": user_id, "room_id": room_id}
            ).first()
            questions = Exam.objects(room_id=room_id).first()
            return render_template("exam.html", questions=questions, room=room)
    return redirect(url_for("auth.login"))


@user.route("/result", methods=["POST"])
def check_answer():
    questions = request.form.to_dict()
    result = []
    """
    for question, answer in questions.items():
        q = Storage.objects(Id=question).first()
        if q:
            if str(q.correct_answer) == answer:
                result.append(answer)
    """
    return f"correct answer {len(result)}"
