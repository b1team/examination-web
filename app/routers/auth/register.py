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
        return redirect(url_for("home.home"))
    return render_template("register.html")


@auth.route("/register", methods=["POST"])
def register():
    user_info = request.form.to_dict()
    user = user_info.get("username", None)
    email=  user_info.get("email", None)
    gender = user_info.get("sex", None)
    classify = user_info.get("classify", None)
    if not user_info or not user or not email or not gender or not classify:
        flash("Vui lòng điền đầy đủ thông tin", "error")
        return redirect(request.referrer)
    existing_user = User.objects(email=email).first()
    if existing_user is None:
        password = generate_password_hash(user_info.get("password"))
        user = User(
            username=user,
            password=password,
            email=email,
            gender=gender,
            classify=classify,
        )
        user.save()
        return redirect(url_for("auth.login"))

    flash("User already exists")
    return redirect(request.url)
