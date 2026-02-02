# app/forum/__init__.py
from flask import Blueprint

forum_bp = Blueprint('forum', __name__, template_folder='templates')

# Import routes AFTER creating the blueprint
from app.forum import routes