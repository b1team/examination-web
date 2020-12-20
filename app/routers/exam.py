from app.routers.user import user, render_template, session, redirect, url_for


@user.route("/exam-form", methods=["GET"])
def show_exam_form():
    return render_template("createExam.html")
