from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..extensions import db
from ..models import User, Role

admin_bp = Blueprint("admin", __name__, template_folder="../templates/admin")

def admin_required():
    return current_user.is_authenticated and current_user.is_admin()

@admin_bp.route("/staff", methods=["GET", "POST"])
@login_required
def staff():
    if not admin_required():
        flash("Admin only.", "danger")
        return redirect(url_for("appointments.list_appointments"))
    if request.method == "POST":
        user_id = request.form.get("user_id")
        role = request.form.get("role")
        user = User.query.get_or_404(user_id)
        if role in (Role.PATIENT, Role.STAFF, Role.ADMIN):
            user.role = role
            db.session.commit()
            flash("Role updated.", "success")
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/staff.html", users=users, roles=[Role.PATIENT, Role.STAFF, Role.ADMIN])
