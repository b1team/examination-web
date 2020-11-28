from app.routers.auth import (
    auth,
    render_template,
    request,
    url_for,
    redirect,
    generate_password_hash,
    User,
)


@auth.route('/register', methods=["GET"])
def register_form():
    return render_template('register.html')


@auth.route('/register', methods=["POST"])
def register():
    user_info = request.form.to_dict()
    user = User.objects(email=user_info.get("email"),
                        username=user_info.get('username')).first()
    if not user:
        password = generate_password_hash(user_info.get('password'))
        user = User(
            username=user_info.get('username'),
            password=password,
            email=user_info.get('email'),
            gender=user_info.get('sex'),
            classify=user_info.get('classify')
        )
        user.save()
        return redirect(url_for('auth.login'))
    return 'alert existing'