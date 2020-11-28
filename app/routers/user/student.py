from app.routers.user import user, render_template

@user.route('/student', methods=["GET"])
def student_form():
    return render_template('student.html')
