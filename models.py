from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from config import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Relationships
    decks = db.relationship('Deck', back_populates='user', cascade='all, delete-orphan')
    user_progress = db.relationship('UserProgress', back_populates='user', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Deck(db.Model):
    __tablename__ = 'decks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    subject = db.Column(db.String(50))
    category = db.Column(db.String(50))
    difficulty = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship("User", back_populates="decks")
    flashcards = db.relationship("Flashcard", back_populates="deck", cascade="all, delete-orphan")

    __table_args__ = (db.UniqueConstraint("user_id", "title", name="uq_user_deck_title"),)

    def __repr__(self):
        return f'<Deck {self.title}>'


class Flashcard(db.Model):
    __tablename__ = 'flashcards'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    hint = db.Column(db.String, nullable=True)
    difficulty = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deck_id = db.Column(db.Integer, db.ForeignKey('decks.id', ondelete="CASCADE"), nullable=False)

    # Relationships
    deck = db.relationship('Deck', back_populates='flashcards')
    progress = db.relationship('UserProgress', back_populates='flashcard', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Flashcard {self.question[:50]}>'


class UserProgress(db.Model):  # Renamed from 'Progress' to 'UserProgress'
    __tablename__ = 'user_progress'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    flashcard_id = db.Column(db.Integer, db.ForeignKey('flashcards.id', ondelete="CASCADE"), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='user_progress')
    flashcard = db.relationship('Flashcard', back_populates='progress')

    def __repr__(self):
        status = 'Correct' if self.is_correct else 'Incorrect'
        return f'<UserProgress User: {self.user_id}, Flashcard: {self.flashcard_id}, Status: {status}>'
