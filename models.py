from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from config import db  # ✅ Use the initialized db instance



class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    decks = db.relationship('Deck', back_populates='user', cascade='all, delete-orphan')
    progress = db.relationship('UserProgress', back_populates='user', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Deck(db.Model):
    __tablename__ = 'decks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='decks')
    flashcards = db.relationship('Flashcard', back_populates='deck', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Deck {self.name}>'

class Flashcard(db.Model):
    __tablename__ = 'flashcards'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    deck_id = db.Column(db.Integer, db.ForeignKey('decks.id'), nullable=False)
    deck = db.relationship('Deck', back_populates='flashcards')
    progress = db.relationship('UserProgress', back_populates='flashcard', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Flashcard {self.question[:50]}>'

class Progress(db.Model):
    __tablename__ = 'user_progress'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    flashcard_id = db.Column(db.Integer, db.ForeignKey('flashcards.id'), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', back_populates='progress')
    flashcard = db.relationship('Flashcard', back_populates='progress')

    def __repr__(self):
        status = 'Correct' if self.is_correct else 'Incorrect'
        return f'<UserProgress User: {self.user_id}, Flashcard: {self.flashcard_id}, Status: {status}>'
