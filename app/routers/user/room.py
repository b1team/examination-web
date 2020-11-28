from app.routers.user import user, render_template, session, redirect, url_for


@user.route("/room")
def room_form():
    return render_template("room.html")
