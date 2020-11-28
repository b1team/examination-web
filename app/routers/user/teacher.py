from app.routers.user import user, render_template, session, redirect, url_for

@user.route('/teacher', methods=['GET'])
def teacher_form():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    username = session['user'].get('username')
    return render_template('teacher.html', username=username)


@user.route('/teacher', methods=['POST'])
def teacher():
    pass