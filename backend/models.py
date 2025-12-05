from datetime import datetime
from flask_login import UserMixin
from .extensions import db

# --- Roles ---
class Role:
    PATIENT = "patient"
    STAFF = "staff"
    ADMIN = "admin"
    DOCTOR = "doctor"   # ✅ Added doctor role


# --- User model ---
class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default=Role.PATIENT, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ✅ Link to Doctor if this user is a doctor
    doctor = db.relationship("Doctor", back_populates="user", uselist=False)

    def is_staff(self):
        return self.role in (Role.STAFF, Role.ADMIN)

    def is_admin(self):
        return self.role == Role.ADMIN

    def is_doctor(self):
        return self.role == Role.DOCTOR

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"


# --- Doctor model ---
class Doctor(db.Model):
    __tablename__ = "doctor"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    specialty = db.Column(db.String(150), nullable=True)

    # ✅ Link back to User
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True)
    user = db.relationship("User", back_populates="doctor")

    appointments = db.relationship("Appointment", backref="doctor", lazy=True)

    def __repr__(self):
        return f"<Doctor {self.name} ({self.specialty})>"


# --- Appointment status constants ---
class AppointmentStatus:
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELED = "canceled"


# --- Appointment model ---
class Appointment(db.Model):
    __tablename__ = "appointment"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"), nullable=False)

    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    reason = db.Column(db.String(255))
    status = db.Column(db.String(20), default=AppointmentStatus.PENDING, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship("User", foreign_keys=[patient_id], backref="appointments")
    staff = db.relationship("User", foreign_keys=[staff_id])

    @property
    def starts_at(self):
        return datetime.combine(self.date, self.time)

    def __repr__(self):
        return (
            f"<Appointment {self.date} {self.time} "
            f"Doctor={self.doctor_id} Patient={self.patient_id} Status={self.status}>"
        )
