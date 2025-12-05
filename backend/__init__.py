from flask import Flask
from .extensions import db, login_manager, migrate
from config import Config
from .models import User, Doctor, Appointment   # import all models so migrations can detect them

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)        # ✅ Flask-Migrate wired in
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # 🔑 Add user_loader so Flask-Login knows how to fetch users
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import blueprints
    from .auth.routes import auth_bp
    from .appointments.routes import appt_bp
    from .admin.routes import admin_bp

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(appt_bp, url_prefix="/appointments")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # Default route
    @app.route("/")
    def index():
        return "<h3>Clinic Booking System</h3><p><a href='/auth/login'>Login</a></p>"

    return app
