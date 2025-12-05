from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime

from ..extensions import db
from ..models import Appointment, AppointmentStatus, Doctor
from .forms import BookForm

appt_bp = Blueprint("appointments", __name__, template_folder="../templates/appointments")


@appt_bp.route("/book", methods=["GET", "POST"])
@login_required
def book():
    form = BookForm()

    # Load doctors and set choices for SelectField
    doctors = Doctor.query.order_by(Doctor.name).all()
    form.doctor_id.choices = [(d.id, f"{d.name} — {d.specialty or 'General'}") for d in doctors]

    if form.validate_on_submit():
        # Prevent duplicate appointment at same date/time for this patient
        exists = Appointment.query.filter_by(
            patient_id=current_user.id,
            date=form.date.data,
            time=form.time.data
        ).first()
        if exists:
            flash("You already have an appointment at this time.", "warning")
        else:
            # Verify doctor exists
            doctor = Doctor.query.get(form.doctor_id.data)
            if not doctor:
                flash("Selected doctor not found. Please choose a valid doctor.", "danger")
                return redirect(url_for("appointments.book"))

            appt = Appointment(
                patient_id=current_user.id,
                doctor_id=doctor.id,
                date=form.date.data,
                time=form.time.data,
                reason=form.reason.data or None,
                status=AppointmentStatus.PENDING,
                created_at=datetime.utcnow()
            )
            db.session.add(appt)
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
                flash("Could not create appointment. Please try again.", "danger")
                return redirect(url_for("appointments.book"))

            flash("Appointment requested. Awaiting staff approval.", "success")
            return redirect(url_for("appointments.list_appointments"))

    return render_template("appointments/book.html", form=form, doctors=doctors)


@appt_bp.route("/list")
@login_required
def list_appointments():
    if current_user.is_staff():
        q = Appointment.query.order_by(Appointment.date.desc(), Appointment.time.desc())
    else:
        q = Appointment.query.filter_by(patient_id=current_user.id) \
                             .order_by(Appointment.date.desc(), Appointment.time.desc())
    appointments = q.all()
    return render_template("appointments/list.html", appointments=appointments)


@appt_bp.route("/cancel/<int:appt_id>", methods=["POST"])
@login_required
def cancel(appt_id):
    appt = Appointment.query.get_or_404(appt_id)
    if appt.patient_id != current_user.id and not current_user.is_staff():
        flash("Not authorized to cancel this appointment.", "danger")
        return redirect(url_for("appointments.list_appointments"))
    appt.status = AppointmentStatus.CANCELED
    db.session.commit()
    flash("Appointment canceled.", "info")
    return redirect(url_for("appointments.list_appointments"))


@appt_bp.route("/approve/<int:appt_id>", methods=["POST"])
@login_required
def approve(appt_id):
    if not current_user.is_staff():
        flash("Staff only.", "danger")
        return redirect(url_for("appointments.list_appointments"))
    appt = Appointment.query.get_or_404(appt_id)
    appt.status = AppointmentStatus.APPROVED
    appt.staff_id = current_user.id
    db.session.commit()
    flash("Appointment approved.", "success")
    return redirect(url_for("appointments.manage"))


@appt_bp.route("/reject/<int:appt_id>", methods=["POST"])
@login_required
def reject(appt_id):
    if not current_user.is_staff():
        flash("Staff only.", "danger")
        return redirect(url_for("appointments.list_appointments"))
    appt = Appointment.query.get_or_404(appt_id)
    appt.status = AppointmentStatus.REJECTED
    db.session.commit()
    flash("Appointment rejected.", "warning")
    return redirect(url_for("appointments.manage"))


@appt_bp.route("/manage")
@login_required
def manage():
    if not current_user.is_staff():
        flash("Staff only.", "danger")
        return redirect(url_for("appointments.list_appointments"))
    appointments = Appointment.query.order_by(Appointment.date, Appointment.time).all()
    return render_template("appointments/manage.html", appointments=appointments)


@appt_bp.route("/dashboard")
@login_required
def dashboard():
    if not current_user.is_staff():
        flash("Staff only.", "danger")
        return redirect(url_for("appointments.list_appointments"))

    pending_count = Appointment.query.filter_by(status=AppointmentStatus.PENDING).count()
    approved_count = Appointment.query.filter_by(status=AppointmentStatus.APPROVED).count()
    canceled_count = Appointment.query.filter_by(status=AppointmentStatus.CANCELED).count()

    appointments = Appointment.query.order_by(Appointment.date, Appointment.time).all()

    return render_template(
        "appointments/dashboard.html",
        pending_count=pending_count,
        approved_count=approved_count,
        canceled_count=canceled_count,
        appointments=appointments
    )


@appt_bp.route("/calendar")
@login_required
def calendar():
    if not current_user.is_staff():
        flash("Staff only.", "danger")
        return redirect(url_for("appointments.list_appointments"))

    appointments = Appointment.query.order_by(Appointment.date, Appointment.time).all()
    appointments_by_date = {}
    for a in appointments:
        appointments_by_date.setdefault(a.date, []).append(a)

    return render_template("appointments/calendar.html", appointments_by_date=appointments_by_date)


# ✅ Doctor Dashboard route
@appt_bp.route("/doctor_dashboard")
@login_required
def doctor_dashboard():
    if not current_user.is_doctor():
        flash("Doctors only.", "danger")
        return redirect(url_for("appointments.list_appointments"))

    # Show appointments assigned to this doctor
    appointments = Appointment.query.filter_by(doctor_id=current_user.doctor.id).order_by(
        Appointment.date, Appointment.time
    ).all()

    return render_template("appointments/doctor_dashboard.html", appointments=appointments)
