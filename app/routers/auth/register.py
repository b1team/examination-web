from app.routers.auth import (
    auth,
    render_template,
    request,
    url_for,
    redirect,
    session,
    flash,
    generate_password_hash,
    User,
)


@auth.route("/register", methods=["GET"])
def register_form():
    if session.get("user", None):
        return redirect(url_for(f"user.user_form"))
    return render_template("register.html")


@auth.route("/register", methods=["POST"])
def register():
    user_info = request.form.to_dict()
    existing_user = User.objects(email=user_info.get("email")).first()

    if existing_user is None:
        password = generate_password_hash(user_info.get("password"))
        user = User(
            username=user_info.get("username"),
            password=password,
            email=user_info.get("email"),
            gender=user_info.get("sex"),
            classify=user_info.get("classify"),
        )
        user.save()
        return redirect(url_for("auth.login"))

    flash("User already exists")
    return redirect(request.url)
