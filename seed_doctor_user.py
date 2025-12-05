from backend import create_app
from backend.extensions import db
from backend.models import User, Role, Doctor
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    email = "ali.khan@example.com"

    # Check if user already exists
    doctor_user = User.query.filter_by(email=email).first()
    if doctor_user:
        print(f"User {email} already exists, updating role and password...")
        doctor_user.role = Role.DOCTOR
        doctor_user.name = "Dr. Ali Khan"
        doctor_user.password_hash = generate_password_hash("password123")
    else:
        print(f"Creating new doctor user {email}...")
        doctor_user = User(
            name="Dr. Ali Khan",
            email=email,
            password_hash=generate_password_hash("password123"),
            role=Role.DOCTOR
        )
        db.session.add(doctor_user)

    db.session.commit()

    # Check if doctor record exists
    doctor = Doctor.query.filter_by(user_id=doctor_user.id).first()
    if doctor:
        print("Doctor record already exists, updating...")
        doctor.name = "Dr. Ali Khan"
        doctor.specialty = "Cardiology"
    else:
        print("Creating new doctor record...")
        doctor = Doctor(
            name="Dr. Ali Khan",
            specialty="Cardiology",
            user_id=doctor_user.id
        )
        db.session.add(doctor)

    db.session.commit()

    print("✅ Doctor user and doctor record ready!")
    print(f"Login with email: {doctor_user.email}, password: password123")
