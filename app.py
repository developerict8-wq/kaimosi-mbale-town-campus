import os

from flask import Flask
from extensions import db, login_manager


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # =========================================================
    # DIRECTORIES
    # =========================================================
    os.makedirs(app.instance_path, exist_ok=True)

    os.makedirs(
        os.path.join(app.root_path, "static", "uploads"),
        exist_ok=True
    )

    # =========================================================
    # SECRET KEY
    # =========================================================
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY",
        "change-this-secret-key"
    )

    # =========================================================
    # DATABASE
    # =========================================================
    database_url = os.environ.get("DATABASE_URL")

    if database_url:
        # Render / PostgreSQL
        if database_url.startswith("postgres://"):
            database_url = database_url.replace(
                "postgres://",
                "postgresql://",
                1
            )

        app.config["SQLALCHEMY_DATABASE_URI"] = database_url

    else:
        # Local development / SQLite
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            "sqlite:///" +
            os.path.join(app.instance_path, "school.db")
        )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # =========================================================
    # FILE UPLOADS
    # =========================================================
    app.config["UPLOAD_FOLDER"] = os.path.join(
        app.root_path,
        "static",
        "uploads"
    )

    app.config["MAX_CONTENT_LENGTH"] = 32 * 1024 * 1024

    # =========================================================
    # INITIALIZE EXTENSIONS
    # =========================================================
    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "admin.login"

    login_manager.login_message = (
        "Please log in to access the administration area."
    )

    # =========================================================
    # IMPORT ALL MODELS
    # =========================================================
    import models

    from models import Admin, SchoolInfo

    # =========================================================
    # IMPORT ROUTES
    # =========================================================
    from routes.admin import admin_bp
    from routes.public import public_bp

    app.register_blueprint(admin_bp)
    app.register_blueprint(public_bp)

    # =========================================================
    # FLASK-LOGIN USER LOADER
    # =========================================================
    @login_manager.user_loader
    def load_user(user_id):
        try:
            return db.session.get(Admin, int(user_id))
        except (ValueError, TypeError):
            return None

    # =========================================================
    # DATABASE INITIALIZATION
    # =========================================================
    with app.app_context():

        # Create all database tables
        db.create_all()

        # -----------------------------------------------------
        # DEFAULT ADMINISTRATOR
        # -----------------------------------------------------
        admin = Admin.query.filter_by(
            username="admin"
        ).first()

        if not admin:

            admin_password = os.environ.get(
                "ADMIN_PASSWORD",
                "admin123"
            )

            admin = Admin(
                username="admin",
                full_name="System Administrator"
            )

            admin.set_password(admin_password)

            db.session.add(admin)

        # -----------------------------------------------------
        # SCHOOL INFORMATION
        # -----------------------------------------------------
        school = SchoolInfo.query.first()

        if not school:

            school = SchoolInfo(
                school_name=(
                    "KAIMOSI NATIONAL POLYTECHNIC "
                    "– MBALE TOWN CAMPUS"
                ),

                motto="Excellence in Education",

                about=(
                    "Welcome to Kaimosi National Polytechnic "
                    "– Mbale Town Campus."
                ),

                vision=(
                    "To be a leading centre of excellence in "
                    "technical and vocational education."
                ),

                mission=(
                    "To provide quality technical and vocational "
                    "education and training for sustainable "
                    "development."
                ),

                values=(
                    "Integrity, Discipline, Excellence, Respect, "
                    "Teamwork and Innovation"
                )
            )

            db.session.add(school)

        # Save changes
        db.session.commit()

    return app


# =============================================================
# APPLICATION INSTANCE
# =============================================================
app = create_app()


# =============================================================
# LOCAL DEVELOPMENT SERVER
# =============================================================
if __name__ == "__main__":

    print("=" * 60)
    print(" SCHOOL WEBSITE SERVER")
    print("=" * 60)

    print(" Local:")
    print(" http://127.0.0.1:5000")

    print()

    print(" Admin:")
    print(" http://127.0.0.1:5000/admin/login")

    print()

    print(" Network:")
    print(" http://192.168.18.12:5000")

    print("=" * 60)

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )