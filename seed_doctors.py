from backend import create_app
from backend.extensions import db
from backend.models import Doctor

app = create_app()

with app.app_context():
    doctors = [
        Doctor(name="Dr. Ali Khan", specialty="Cardiology"),
        Doctor(name="Dr. Fatima Ahmed", specialty="Dermatology"),
        Doctor(name="Dr. Hassan Raza", specialty="Pediatrics"),
        Doctor(name="Dr. Sara Malik", specialty="Neurology"),
        Doctor(name="Dr. Imran Siddiqui", specialty="Orthopedics"),
    ]

    db.session.add_all(doctors)
    db.session.commit()

    print("✅ Doctors seeded successfully!")
    for d in Doctor.query.all():
        print(f"{d.id}: {d.name} — {d.specialty}")