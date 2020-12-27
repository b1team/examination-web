from app.routers.user import (
    user,
    render_template,
)


@user.route("/error", methods=["GET"])
def error():
    return render_template("error.html")
