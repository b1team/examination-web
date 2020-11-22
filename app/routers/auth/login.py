from app.routers.auth import (
    auth,
    render_template,
    request,
    url_for,
    redirect,
    session,
    check_password_hash,
    User,
)


@auth.route("/login", methods=["GET"])
def login_form():
    if "user" in session:
        # TODO redirect to ...
        return "you was logged"
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def login():
    user_info = request.form.to_dict()
    user = User.objects(username=user_info.get("username")).first()
    if user and check_password_hash(
        user["password"], user_info.get("password")
    ):
        return "ok"
    return "not"
