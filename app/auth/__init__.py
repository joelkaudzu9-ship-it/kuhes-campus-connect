# app/auth/__init__.py
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

# Import routes AFTER creating the blueprint
# This is the standard Flask pattern
from app.auth import routes