from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    theme = db.Column(db.String(140))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.String(140))
    
    THEMES = ["race", "nourriture", "jeux"]

    def __init__(self, title, theme, body, author_id, timestamp):
        if theme not in self.THEMES:
            raise ValueError(f"Le thème doit être l'un des suivants : {', '.join(self.THEMES)}")
        self.title = title
        self.theme = theme
        self.body = body
        self.author_id = author_id
        self.timestamp = timestamp