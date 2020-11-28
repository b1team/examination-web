from flask import Blueprint, session, render_template, redirect, url_for

bp = Blueprint("home", __name__, url_prefix="/")


@bp.route("/", methods=["GET"])
def home():
    return render_template("index.html", session=session.get("user", None))


@bp.route("/start", methods=["GET"])
def start():
    return redirect(url_for(f"user.user_form"))
