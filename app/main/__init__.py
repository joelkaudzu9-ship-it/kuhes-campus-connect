# app/main/__init__.py
from flask import Blueprint

main_bp = Blueprint('main', __name__)

# Import routes AFTER creating the blueprint
from app.main import routes