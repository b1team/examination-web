from app.routers.auth import (
    auth,
    render_template,
    request,
    url_for,
    redirect,
    session,
    flash,
    check_password_hash,
    User,
)


@auth.route("/login", methods=["GET"])
def login_form():
    if session.get("user", None):
        return redirect(url_for("home.home"))
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def login():
    user_info = request.form.to_dict()
    user = User.objects(username=user_info.get("username")).first()

    if user and check_password_hash(user.password, user_info.get("password")):
        session["user"] = {
            "username": user.username,
            "classify": user.classify,
            "user_id": str(user.user_id),
        }
        return redirect(url_for(f"user.{user.classify}_form"))

    flash("username or password is incorrect")
    return redirect(request.url)


@auth.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
