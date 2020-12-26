from app.routers.user import user, render_template, session, redirect, url_for


@user.route("/form-exam", methods=["GET"])
def show_exam_form():
    if session.get("user", None):
        if session["user"].get("classify") == "teacher":
            return render_template("formExam.html")
    return redirect(url_for("auth.login"))