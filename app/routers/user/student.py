from app.routers.user import user
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
from app.models.room import Room


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
        rooms = Room.objects(student__student_id=user_id).exclude("student")
        return render_template("student.html", username=username, rooms=rooms)
    return redirect(url_for("auth.login"))
