# app/events/__init__.py
from flask import Blueprint

events_bp = Blueprint('events', __name__, template_folder='templates')

# Import routes AFTER creating the blueprint
from app.events import routes