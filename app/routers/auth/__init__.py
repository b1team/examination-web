from flask import Blueprint, session, render_template, request, redirect, url_for
from app.models.user import User
from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint('auth', __name__)
