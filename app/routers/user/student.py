from app.routers.user import user
from bson import ObjectId
from app.routers.user import (
    render_template,
    session,
    redirect,
    url_for,
    request,
)
from random import shuffle
from jinja2 import environment
from app.models.room import Room
from app.models.exam import Exam


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
        if session["user"].get("classify") == "student":
            username = session["user"].get("username")
            user_id = ObjectId(session["user"].get("user_id"))
            rooms = Room.objects(student__student_id=user_id).exclude(
                "student"
            )
            return render_template(
                "student.html", username=username, rooms=rooms
            )
    return redirect(url_for("auth.login"))


@user.route("/student-room", methods=["GET"])
def student_room():
    if session.get("user", None):
        if session["user"].get("classify") == "student":
            info = request.args.to_dict()
            room_id = ObjectId(info.get("rid"))
            user_id = ObjectId(session["user"].get("user_id"))
            room = Room.objects(
                room_id=room_id, student__student_id=user_id
            ).first()
            exams = Exam.objects(room_id=room_id).only("duration", "exam_name")
            return render_template("studentRoom.html", room=room, exams=exams)
    return redirect(url_for("auth.login"))
