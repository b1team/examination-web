from app.routers.user import (
    user,
    request,
    render_template,
    session,
    redirect,
    url_for,
)
from random import choice, shuffle
import string
from app.models.room import Room, Teacher, Student
from bson import ObjectId


@user.route("/room", methods=["GET"])
def room_form():
    if session.get("user", None):
        if session["user"].get("classify") == "teacher":
            return render_template("room.html")
    return redirect(url_for("home.home"))


def random_code():
    chars = [string.ascii_lowercase, string.ascii_uppercase, string.digits]
    result = [choice(char) for char in chars]
    for _ in range(5):
        result.append(choice("".join(chars)))
    shuffle(result)
    result = "".join(result)
    return result


@user.route("/room", methods=["POST"])
def create_room():
    room_info = request.form.to_dict()
    room_code = random_code()
    teacher = Teacher(
        teacher_id=ObjectId(session["user"].get("user_id")),
        teacher_name=session["user"].get("username"),
    )
    new_room = Room(
        room_name=room_info.get("classname"),
        subject=room_info.get("subject"),
        teacher=teacher,
        room_code=room_code,
    )
    new_room.save()
    return redirect(url_for("user.teacher_form"))


@user.route("/join-room/<room_id>", methods=["POST"])
def join_room(room_id=None):
    student_name = session["user"].get("username")
    student_id = session["user"].get("user_id")
    room = Room.objects.get_or_404(room_id=room_id)
    if room:
        new_student = Student(
            student_id=student_id,
            student_name=student_name
        )
        Room.objects(room_id=room_id).update(push__student=new_student)
        return redirect(url_for("user.student_form"))


@user.route("/student/search", methods=["GET"])
def search():
    room_code = request.args.get("q")
    room = Room.objects.get_or_404(room_code=room_code)
    return render_template("search.html", room=room)