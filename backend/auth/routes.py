from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from ..extensions import db
from ..models import User, Role
from .forms import LoginForm, RegisterForm

auth_bp = Blueprint("auth", __name__, template_folder="../templates/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect_after_login(current_user)

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash("Logged in successfully.", "success")

            # Support ?next= redirect
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            return redirect_after_login(user)

        flash("Invalid email or password.", "danger")

    return render_template("auth/login.html", form=form)


def redirect_after_login(user):
    """Redirect user after login based on role."""
    if hasattr(user, "is_admin") and user.is_admin():
        return redirect(url_for("appointments.dashboard"))
    if hasattr(user, "is_staff") and user.is_staff():
        return redirect(url_for("appointments.dashboard"))
    return redirect(url_for("appointments.list_appointments"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already registered.", "warning")
        else:
            user = User(
                name=form.name.data,
                email=form.email.data,
                password_hash=generate_password_hash(form.password.data),
                role=Role.PATIENT,
            )
            db.session.add(user)
            db.session.commit()
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
