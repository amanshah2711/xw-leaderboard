
from . import db, bcrypt
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint
import os


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    invite_link = db.Column(db.String(200), unique=True, nullable=False)
    encrypted_nyt_cookie = db.Column(db.String(500), nullable=True)

    games = db.relationship('CrosswordData', backref='user', foreign_keys='[CrosswordData.user_id]', lazy='dynamic')

    friends_one = relationship('Friends', backref='user_one', foreign_keys='[Friends.friend_one]', lazy='dynamic')
    friends_two = relationship('Friends', backref='user_two', foreign_keys='[Friends.friend_two]', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8') 

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password) 

class CrosswordData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    day = db.Column(db.Date, nullable=False)
    solve_time = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='incomplete')
    kind = db.Column(db.String(20), nullable=False, default='daily')
    
    __table_args__ = (UniqueConstraint("user_id", "day", name="unique_user_day"),)

class Friends(db.Model):
    friend_one = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    friend_two = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
