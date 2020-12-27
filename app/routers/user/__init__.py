from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    request,
)

user = Blueprint("user", __name__)
