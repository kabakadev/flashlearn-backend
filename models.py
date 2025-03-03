from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from config import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    decks = db.relationship('Deck', backref='user', lazy=True, cascade='all, delete-orphan')
    progress = db.relationship('Progress', backref='user', lazy=True, cascade='all, delete-orphan')
    stats = db.relationship('UserStats', backref='user', lazy=True, uselist=False, cascade='all, delete-orphan')
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
        
    @password.setter
    def password_hash(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Deck(db.Model):
    __tablename__ = 'decks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    is_default = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    flashcards = db.relationship('Flashcard', backref='deck', lazy=True, cascade='all, delete-orphan')
    progress = db.relationship('Progress', backref='deck', lazy=True, cascade='all, delete-orphan')

class Flashcard(db.Model):
    __tablename__ = 'flashcards'
    
    id = db.Column(db.Integer, primary_key=True)
    deck_id = db.Column(db.Integer, db.ForeignKey('decks.id'), nullable=False)
    front_text = db.Column(db.Text, nullable=False)
    back_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    progress = db.relationship('Progress', backref='flashcard', lazy=True, cascade='all, delete-orphan')

class Progress(db.Model):
    __tablename__ = 'progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    deck_id = db.Column(db.Integer, db.ForeignKey('decks.id'), nullable=False)
    flashcard_id = db.Column(db.Integer, db.ForeignKey('flashcards.id'), nullable=False)
    study_count = db.Column(db.Integer, default=0)
    correct_attempts = db.Column(db.Integer, default=0)
    incorrect_attempts = db.Column(db.Integer, default=0)
    total_study_time = db.Column(db.Float, default=0.0)  # in minutes
    last_studied_at = db.Column(db.DateTime, nullable=True)
    next_review_at = db.Column(db.DateTime, nullable=True)
    review_status = db.Column(db.String(20), default='new')  # new, learning, review, mastered
    is_learned = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserStats(db.Model):
    __tablename__ = 'user_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    weekly_goal = db.Column(db.Integer, default=50)  # Number of cards to study weekly
    mastery_level = db.Column(db.Float, default=0.0)  # Percentage
    study_streak = db.Column(db.Integer, default=0)  # Days in a row
    focus_score = db.Column(db.Float, default=0.0)  # Percentage
    retention_rate = db.Column(db.Float, default=0.0)  # Percentage
    cards_mastered = db.Column(db.Integer, default=0)
    minutes_per_day = db.Column(db.Float, default=0.0)
    accuracy = db.Column(db.Float, default=0.0)  # Percentage
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)