from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from ..extensions import db
from ..models import User, Role, Doctor

admin_bp = Blueprint("admin", __name__, template_folder="../templates/admin")

def is_admin_user():
    return current_user.is_authenticated and current_user.is_admin()

@admin_bp.route("/staff", methods=["GET", "POST"])
@login_required
def staff():
    if not is_admin_user():
        flash("Admin only.", "danger")
        return redirect(url_for("appointments.list_appointments"))
    if request.method == "POST":
        user_id = request.form.get("user_id")
        role = request.form.get("role")
        user = User.query.get_or_404(user_id)
        if role in (Role.PATIENT, Role.STAFF, Role.ADMIN, Role.DOCTOR):
            user.role = role
            db.session.commit()
            flash("Role updated.", "success")
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/staff.html", users=users, roles=[Role.PATIENT, Role.STAFF, Role.ADMIN, Role.DOCTOR])

@admin_bp.route("/doctors", methods=["GET", "POST"])
@login_required
def manage_doctors():
    if not is_admin_user():
        flash("Admin only.", "danger")
        return redirect(url_for("appointments.list_appointments"))

    if request.method == "POST":
        action = request.form.get("action")
        if action == "add":
            user_id = request.form.get("user_id")
            specialty = request.form.get("specialty")
            bio = request.form.get("bio")

            user = User.query.get_or_404(user_id)
            if user.role != Role.DOCTOR:
                flash("User must have Doctor role first.", "warning")
            else:
                existing_doctor = Doctor.query.filter_by(user_id=user.id).first()
                if existing_doctor:
                    existing_doctor.specialty = specialty
                    existing_doctor.bio = bio
                    flash("Doctor profile updated.", "success")
                else:
                    new_doctor = Doctor(name=user.name, specialty=specialty, bio=bio, user_id=user.id)
                    db.session.add(new_doctor)
                    flash("Doctor profile created.", "success")
                db.session.commit()

        elif action == "delete":
            doctor_id = request.form.get("doctor_id")
            doctor = Doctor.query.get_or_404(doctor_id)
            db.session.delete(doctor)
            db.session.commit()
            flash("Doctor record removed (User remains).", "info")

    doctors = Doctor.query.all()
    # Users with DOCTOR role who don't have a Doctor record yet
    doctor_users = User.query.filter_by(role=Role.DOCTOR).all()

    return render_template("admin/manage_doctors.html", doctors=doctors, doctor_users=doctor_users)
