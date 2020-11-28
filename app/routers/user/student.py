from app.routers.user import user


@user.route("/student", methods=["POST"])
def student():
    pass
