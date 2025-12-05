from backend import create_app
from backend.extensions import db
from backend.models import User, Role
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    email = "staff@example.com"

    # Check if staff user already exists
    staff_user = User.query.filter_by(email=email).first()
    if staff_user:
        print(f"User {email} already exists, updating role and password...")
        staff_user.role = Role.STAFF
        staff_user.name = "Clinic Staff"
        staff_user.password_hash = generate_password_hash("password123")
    else:
        print(f"Creating new staff user {email}...")
        staff_user = User(
            name="Clinic Staff",
            email=email,
            password_hash=generate_password_hash("password123"),
            role=Role.STAFF
        )
        db.session.add(staff_user)

    db.session.commit()

    print("✅ Staff user ready!")
    print(f"Login with email: {staff_user.email}, password: password123")
