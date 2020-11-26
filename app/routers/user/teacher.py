from app.routers.user import user, render_template

@user.route('/teacher', methods=['GET'])
def teacher_form():
    return render_template('teacher.html')
