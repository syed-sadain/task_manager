import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")

    # ── Database ──────────────────────────────────────────────
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "3306")
    db_user = os.getenv("DB_USER", "root")
    db_pass = os.getenv("DB_PASSWORD", "Pass@123")
    db_name = os.getenv("DB_NAME", "task_manager_db")

    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:Pass%40123@localhost/task_manager_db"
   
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ── JWT ───────────────────────────────────────────────────
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "fallback-secret")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False   # tokens don't expire (demo)

    # ── General ───────────────────────────────────────────────
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "flask-secret")

    db.init_app(app)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # ── Blueprints ────────────────────────────────────────────
    from backend.routes.auth import auth_bp
    from backend.routes.tasks import tasks_bp
    from backend.routes.views import views_bp

    app.register_blueprint(auth_bp,  url_prefix="/api/auth")
    app.register_blueprint(tasks_bp, url_prefix="/api/tasks")
    app.register_blueprint(views_bp)

    # ── Create tables ─────────────────────────────────────────
    with app.app_context():
        db.create_all()

    return app
