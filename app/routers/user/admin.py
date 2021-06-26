from app.routers.user import user
from bson import ObjectId
from app.routers.user import (
    render_template,
    session,
    redirect,
    url_for,
    request,
)
from random import shuffle
from jinja2 import environment
from app.models.room import Room
from app.models.exam import Exam

@user.route("/admin", methods=["GET"])
def admin():
    return render_template('admin.html')