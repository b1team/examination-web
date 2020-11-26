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


@auth.route('/register', methods=["GET"])
def register_form():
    return render_template('register.html')


@auth.route('/register', methods=["POST"])
def register():
    user_info = request.form.to_dict()
    print(user_info)
    return 'OK'