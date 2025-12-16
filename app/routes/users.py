from flask import Blueprint, jsonify,render_template, session, redirect, url_for
from app.models import User

bp = Blueprint('users', __name__)



@bp.route("/dashboard", methods=["GET"])
def user_dashboard():
    email = session.get("email")  
    if not email:
        return redirect("/auth/login")

    user = User.query.filter_by(email=email).first()
    if not user:
        return redirect("/auth/login")

    return render_template("user_dashboard.html", name=user.name)


@bp.route('/logout')
def logout():
    session.pop('user_login', None)
    session.pop('user_id', None)
    session.pop('user_email', None)
    session.pop('registration_data', None)
    return redirect(url_for('home'))