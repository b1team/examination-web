from app.routers.user import user
from bson import ObjectId
from app.routers.user import (
    render_template,
    session,
    redirect,
    url_for,
    request,
)
from app.models.room import Room
from app.models.user import User
import re

@user.route("/admin", methods=["GET"])
def admin_form():
    if session.get("user", None):
        classify = session["user"].get("classify")
        if classify in ["student", "teacher"]:
            return redirect(url_for(f"user.{classify}_form"))
    param = request.args.to_dict()
    users = User.objects(classify='teacher').all()
    indexs = [i+1 for i in range(len(users))]
    num_of_room = []
    for user in users:
        room = Room.objects(
                    **{"teacher__teacher_id": user.user_id}
                ).all()
        num_of_room.append(len(room))
    mapper = list(zip(indexs, users, num_of_room))
    return render_template('admin.html', mapper=mapper)

@user.route("/admin/detail", methods=['GET'])
def admin_detail():
    if session.get("user", None):
        classify = session["user"].get("classify")
        if classify in ["student", "teacher"]:
            return redirect(url_for(f"user.{classify}_form"))
    param = request.args.to_dict()
    if param.get("tchid") is not None:
        rooms = Room.objects(
                    **{"teacher__teacher_id": ObjectId(param.get("tchid"))}
                ).all()
        indexs = [i+1 for i in range(len(rooms))]
        room_name = [room.room_name for room in rooms]
        room_code = [room.room_code for room in rooms]
        students = [len(room.student) for room in rooms]
        mapper_room = list(zip(indexs, room_name, room_code, students))
    return render_template("detailRoom.html", mapper_room=mapper_room)


@user.route("/admin/delete", methods=['POST'])
def admin_delete():
    if session.get("user", None):
        classify = session["user"].get("classify")
        if classify in ["student", "teacher"]:
            return redirect(url_for(f"user.{classify}_form"))
    if "delete_no" in request.form:
        return redirect(url_for("user.admin_form"))
    elif 'delete_yes' in request.form:
        param = request.args.to_dict()
        room = Room.objects(
                    **{"teacher__teacher_id": ObjectId(param.get("tchid"))}
                ).all()
        room.delete()
        return redirect(url_for("user.admin_form"))


@user.route("/admin/search", methods=["GET"])
def admin_search():
    if session.get("user", None):
        classify = session["user"].get("classify")
        if classify in ["student", "teacher"]:
            return redirect(url_for(f"user.{classify}_form"))
    search_str = request.args.get("q")
    if re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", search_str.strip()):
        users = User.objects(classify='teacher', email=search_str.strip()).all()
        indexs = [i+1 for i in range(len(users))]
        num_of_room = []
        for user in users:
            room = Room.objects(
                        **{"teacher__teacher_id": user.user_id}
                    ).all()
            num_of_room.append(len(room))
        mapper = list(zip(indexs, users, num_of_room))
        return render_template("admin_search.html", mapper=mapper)

    else:
        users = User.objects(classify='teacher', username=search_str.strip()).all()
        indexs = [i+1 for i in range(len(users))]
        num_of_room = []
        for user in users:
            room = Room.objects(
                        **{"teacher__teacher_id": user.user_id}
                    ).all()
            num_of_room.append(len(room))
        mapper = list(zip(indexs, users, num_of_room))
        return render_template("admin_search.html", mapper=mapper)