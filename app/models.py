# app/models.py - FIXED TOP SECTION
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

# Create db instance HERE instead of importing from app
db = SQLAlchemy()


# Import db from the app package
from app import db

# ... rest of your models code ...


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    faculty = db.Column(db.String(100))
    program = db.Column(db.String(100))
    year = db.Column(db.String(20))
    role = db.Column(db.String(20), default='student')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    posts = db.relationship('Post', backref='author', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy=True, cascade='all, delete-orphan')
    events = db.relationship('Event', backref='organizer', lazy=True, cascade='all, delete-orphan',
                           foreign_keys='Event.user_id')
    reactions = db.relationship('PostReaction', backref='user', lazy=True, cascade='all, delete-orphan')
    approved_events = db.relationship('Event', backref='approver', lazy=True,
                                    foreign_keys='Event.approved_by')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def is_admin(self):
        return self.role in ['admin', 'leader']

    def can_approve_events(self):
        return self.role in ['admin', 'leader', 'faculty']

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default='general')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan')
    reactions = db.relationship('PostReaction', backref='post', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Post {self.id} - {self.title[:20]}>'

    def get_reaction_counts(self):
        from collections import defaultdict
        counts = defaultdict(int)
        for reaction in self.reactions:
            counts[reaction.reaction_type] += 1
        return dict(counts)

    def get_user_reaction(self, user_id):
        reaction = PostReaction.query.filter_by(post_id=self.id, user_id=user_id).first()
        return reaction.reaction_type if reaction else None

    def get_comments_count(self):
        return len(self.comments)


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    def __repr__(self):
        return f'<Comment {self.id}>'


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    event_type = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50))
    venue = db.Column(db.String(200), nullable=False)
    organizer_name = db.Column(db.String(100))
    contact_email = db.Column(db.String(120))
    contact_phone = db.Column(db.String(20))
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    approved_at = db.Column(db.DateTime)
    rejection_reason = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Event {self.title}>'

    def is_upcoming(self):
        return self.start_date > datetime.utcnow()

    def is_ongoing(self):
        now = datetime.utcnow()
        if self.end_date:
            return self.start_date <= now <= self.end_date
        return self.start_date.date() == now.date()

    def is_past(self):
        if self.end_date:
            return self.end_date < datetime.utcnow()
        return self.start_date < datetime.utcnow()

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(50))  # post_like, comment, event_approval, etc.
    related_id = db.Column(db.Integer)  # ID of related item (post_id, event_id, etc.)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    user = db.relationship('User', backref='notifications', lazy=True)

    def __repr__(self):
        return f'<Notification {self.id} for user {self.user_id}>'

    def mark_as_read(self):
        self.is_read = True
        db.session.commit()

    @staticmethod
    def create_notification(user_id, title, message, notification_type=None, related_id=None):
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            related_id=related_id
        )
        db.session.add(notification)
        db.session.commit()
        return notification
class PostReaction(db.Model):
    __tablename__ = 'post_reactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    reaction_type = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Notification Model

    # Unique constraint to ensure one reaction per user per post
    __table_args__ = (db.UniqueConstraint('user_id', 'post_id', name='unique_user_post_reaction'),)

    def __repr__(self):
        return f'<Reaction {self.reaction_type} by user {self.user_id} on post {self.post_id}>'