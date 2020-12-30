from app.routers.user import (
    user,
    request,
    session,
    render_template,
    url_for,
    redirect,
)
from bson import ObjectId
from app.models.storage import Storage, Answer
from app.models.room import Room


@user.route("/teacher", methods=["GET"])
def teacher_form():
    if session.get("user", None):
        if session["user"].get("classify") == "teacher":
            username = session["user"].get("username")
            user_id = ObjectId(session["user"].get("user_id"))
            rooms = Room.objects(teacher__teacher_id=user_id).exclude(
                "teacher"
            )
            return render_template(
                "teacher.html", username=username, rooms=rooms
            )
    return redirect(url_for("auth.login"))


@user.route("/question/<room_id>", methods=["GET"])
def question_form(room_id: ObjectId):
    try:
        room = Room.objects(room_id=room_id).first()
        if room:
            if session.get("user", None):
                if session["user"].get("classify") == "teacher":
                    return render_template("createQuestion.html", room=room)
            return redirect(url_for("home.home"))
    except Exception:
        return redirect(url_for("user.error"))


@user.route("/question/<room_id>", methods=["POST"])
def create_question(room_id: None):
    question_info = request.form.to_dict()
    teacher_id = ObjectId(session["user"].get("user_id"))
    result = []
    for index, an in enumerate("ABCD", start=0):
        result.append(Answer(id=index, value=question_info.get(f"answer{an}")))
    room = Room.objects(room_id=room_id).first()
    storage = Storage(
        question=question_info.get("question"),
        teacher_id=teacher_id,
        subject_id=room.subject.subject_id,
        room_id=room.room_id,
        answer=result,
        correct_answer=question_info.get("key"),
        level=question_info.get("level"),
    )
    storage.save()
    return redirect(request.referrer)
