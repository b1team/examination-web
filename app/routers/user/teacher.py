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
        username = session["user"].get("username")
        user_id = ObjectId(session["user"].get("user_id"))
        rooms = Room.objects(teacher__teacher_id=user_id).exclude("teacher")
        return render_template("teacher.html", username=username, rooms=rooms)
    return redirect(url_for("auth.login"))


@user.route("/question", methods=["POST"])
def create_question():
    question_info = request.form.to_dict()
    result = []
    for index, an in enumerate("ABCD", start=0):
        result.append(Answer(id=index, value=question_info.get(f"answer{an}")))
    exam = Storage(
        question=question_info.get("question"),
        answer=result,
        correct_answer=question_info.get("key"),
        level=question_info.get("level"),
    )
    exam.save()
    return redirect(request.referrer)
