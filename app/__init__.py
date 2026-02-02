# app/__init__.py - SIMPLIFIED VERSION
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import timedelta

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'


def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = 'kuhes-campus-connect-2024-secret-key-change-this-later'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kuhes.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    app.config['SESSION_PERMANENT'] = True

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)

    # User loader for Flask-Login
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import and register blueprints
    # The routes are automatically imported via the blueprint __init__.py files
    from app.auth import auth_bp
    from app.main import main_bp
    from app.events import events_bp
    from app.forum import forum_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(events_bp, url_prefix='/events')
    app.register_blueprint(forum_bp, url_prefix='/forum')

    # Create database tables
    with app.app_context():
        db.create_all()

    return app


# Create app instance for Gunicorn
app = create_app()
