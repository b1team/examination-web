from app.routers.user import user
from app.models.storage import Storage
from bson import ObjectId
from app.routers.user import (
    render_template,
    request,
    session,
    redirect,
    url_for,
)
from random import shuffle
from jinja2 import environment
from app.models.room import Room, Student


def filter_shuffle(seq):
    try:
        result = list(seq)
        shuffle(result)
        return result
    except:
        return seq


environment.DEFAULT_FILTERS["shuffle"] = filter_shuffle


@user.route("/student", methods=["GET"])
def student_form():
    if session.get("user", None):
        username = session["user"].get("username")
        user_id = ObjectId(session["user"].get("user_id"))
        rooms = Room.objects()
        return render_template("student.html", username=username, rooms=rooms)
    return redirect(url_for("auth.login"))


@user.route("/exam", methods=["GET"])
def show_exam():
    if session.get("user", None):
        if session["user"].get("classify") == "student":
            exams = Storage.objects()
            return render_template("exam.html", exams=exams)
    return redirect(url_for("auth.login"))


@user.route("/exam", methods=["POST"])
def check_answer():
    ques = request.form.to_dict()
    result = []
    for question, answer in ques.items():
        q = Storage.objects(Id=question).first()
        if q:
            if str(q.correct_answer) == answer:
                result.append(answer)
    return f"correct answer {len(result)}"
