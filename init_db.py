import os
from backend import create_app
from backend.extensions import db
from backend.models import User, Role, Doctor, Appointment
from werkzeug.security import generate_password_hash

def init_db():
    app = create_app()
    with app.app_context():
        print("Initializing database...")
        # In a real app we'd use flask db upgrade,
        # but for a fresh start we can use db.create_all()
        # or just assume migrations are up to date.

        # Ensure Roles are respected (though they are just strings in this app)

        # 1. Create Admin
        admin_email = "admin@example.com"
        admin = User.query.filter_by(email=admin_email).first()
        if not admin:
            print(f"Creating admin: {admin_email}")
            admin = User(
                name="System Admin",
                email=admin_email,
                password_hash=generate_password_hash("admin123"),
                role=Role.ADMIN
            )
            db.session.add(admin)

        # 2. Create Staff
        staff_email = "staff@example.com"
        staff = User.query.filter_by(email=staff_email).first()
        if not staff:
            print(f"Creating staff: {staff_email}")
            staff = User(
                name="Clinic Staff",
                email=staff_email,
                password_hash=generate_password_hash("password123"),
                role=Role.STAFF
            )
            db.session.add(staff)

        # 3. Create Doctors
        doctors_data = [
            {
                "name": "Dr. Ali Khan",
                "email": "ali.khan@example.com",
                "specialty": "Cardiology",
                "bio": "Specialist in heart diseases with over 15 years of experience in clinical cardiology."
            },
            {
                "name": "Dr. Fatima Ahmed",
                "email": "fatima.ahmed@example.com",
                "specialty": "Dermatology",
                "bio": "Expert in skin care and cosmetic dermatology, dedicated to helping patients achieve healthy skin."
            },
            {
                "name": "Dr. Hassan Raza",
                "email": "hassan.raza@example.com",
                "specialty": "Pediatrics",
                "bio": "Compassionate pediatrician focused on child development and preventive healthcare."
            }
        ]

        for d_data in doctors_data:
            user = User.query.filter_by(email=d_data["email"]).first()
            if not user:
                print(f"Creating doctor user: {d_data['email']}")
                user = User(
                    name=d_data["name"],
                    email=d_data["email"],
                    password_hash=generate_password_hash("password123"),
                    role=Role.DOCTOR
                )
                db.session.add(user)
                db.session.flush() # Get user.id

            doctor = Doctor.query.filter_by(user_id=user.id).first()
            if not doctor:
                print(f"Creating doctor record for: {d_data['name']}")
                doctor = Doctor(
                    name=d_data["name"],
                    specialty=d_data["specialty"],
                    bio=d_data["bio"],
                    user_id=user.id
                )
                db.session.add(doctor)
            else:
                # Update bio if exists
                doctor.bio = d_data["bio"]
                doctor.specialty = d_data["specialty"]

        db.session.commit()
        print("✅ Database initialized and seeded successfully!")

if __name__ == "__main__":
    init_db()
