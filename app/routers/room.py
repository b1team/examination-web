from app.routers.user import user,request, render_template, session, redirect, url_for


@user.route("/room", methods=['GET'])
def room_form():
    if session.get("user", None):
        if session["user"].get("classify") == "teacher":
            return render_template("room.html")
    return redirect(url_for("home.home"))

@user.route("/room", methods=["POST"])
def create_room():
    room_info = request.form.to_dict()
    class_name = room_info.get("classname")
    subject - room_info.get("subject")
