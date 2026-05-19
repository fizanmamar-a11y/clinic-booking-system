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
            # Direct doctor creation (User + Doctor profile)
            name = request.form.get("name")
            email = request.form.get("email")
            password = request.form.get("password")
            specialty = request.form.get("specialty")
            bio = request.form.get("bio")

            if User.query.filter_by(email=email).first():
                flash("Email already exists.", "warning")
            else:
                try:
                    new_user = User(
                        name=name,
                        email=email,
                        password_hash=generate_password_hash(password or "password123"),
                        role=Role.DOCTOR # or 'staff' as per prompt, but let's use DOCTOR role for logic
                    )
                    db.session.add(new_user)
                    db.session.flush()

                    new_doctor = Doctor(
                        name=name,
                        specialty=specialty,
                        bio=bio,
                        user_id=new_user.id,
                        is_active=True
                    )
                    db.session.add(new_doctor)
                    db.session.commit()
                    flash(f"Doctor {name} added successfully.", "success")
                except Exception as e:
                    db.session.rollback()
                    flash(f"Error adding doctor: {str(e)}", "danger")

        elif action == "toggle_active":
            doctor_id = request.form.get("doctor_id")
            doctor = Doctor.query.get_or_404(doctor_id)
            doctor.is_active = not doctor.is_active
            db.session.commit()
            status = "activated" if doctor.is_active else "moved to Alumni"
            flash(f"Doctor {doctor.name} {status}.", "info")

    # Only show active doctors here
    doctors = Doctor.query.filter_by(is_active=True).all()
    return render_template("admin/manage_doctors.html", doctors=doctors)

@admin_bp.route("/alumni")
@login_required
def alumni():
    if not is_admin_user():
        flash("Admin only.", "danger")
        return redirect(url_for("appointments.list_appointments"))

    # Show inactive doctors
    alumni_doctors = Doctor.query.filter_by(is_active=False).all()
    return render_template("admin/alumni.html", doctors=alumni_doctors)
