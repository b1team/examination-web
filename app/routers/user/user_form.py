from app.routers.user import (
    user,
    render_template,
    session,
    redirect,
    url_for
)


@user.route("/user", methods=["GET"])
def user_form():
    if session.get("user", None):
        username = session["user"].get("username")
        return render_template(
            f'{session["user"].get("classify")}.html', username=username
        )
    return redirect(url_for("auth.login"))
