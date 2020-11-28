from app.routers.user import user, render_template, session, redirect, url_for


@user.route('/student', methods=["GET"])
def student_form():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    username = session['user'].get('username')
    return render_template('student.html', username=username)


@user.route('/student', methods=["POST"])
def student():
    pass
