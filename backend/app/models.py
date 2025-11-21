from . import db, bcrypt
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from sqlalchemy import UniqueConstraint
import os


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    
    # Account Credentials
    display_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    
    # Account Status
    email_verified = db.Column(db.Boolean, default=False, nullable=False)
    email_verified_at = db.Column(db.DateTime(timezone=True), nullable=True)
    account_status = db.Column(db.String(200), default='pending', nullable=False) # options are active, pending, suspended

    # Account Metadata
    created_at = db.Column(db.DateTime(timezone=True), default = lambda : datetime.now(timezone.utc), nullable=False)
    last_login_at = db.Column(db.DateTime(timezone=True), nullable=True)
    
    # Social 
    invite_link = db.Column(db.String(200), unique=True, nullable=False)

    # NYT
    encrypted_nyt_cookie = db.Column(db.String(500), nullable=True)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8') 

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password) 

class CrosswordData(db.Model):
    __tablename__ = 'crossword_data'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    puzzle_type = db.Column(db.String(20), nullable=False, default='daily')
    day = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='incomplete') #options should be complete, partial, unattempted, unknown
    percent_filled = db.Column(db.Integer, nullable=False)
    solve_time = db.Column(db.Integer, nullable=True)

    last_fetched = db.Column(db.Date, nullable=True)
    
    __table_args__ = (UniqueConstraint("user_id", "day", "puzzle_type", name="unique_user_day"),)

class Friendship(db.Model):
    __tablename__ = 'friendships'

    node_one = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    node_two = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)