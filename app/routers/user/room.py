from app.routers.user import user, render_template, session, redirect, url_for


@user.route("/room")
def room_form():
    if session.get("user", None):
        if session["user"].get("classify") == "teacher":
            return render_template("room.html")
    return redirect(url_for("home.home"))
