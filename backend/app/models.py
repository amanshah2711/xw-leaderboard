
from . import db, bcrypt
from flask_login import UserMixin
from sqlalchemy.orm import relationship


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    # Relationship for friend_one
    friends_one = relationship('Friends', backref='user_one', foreign_keys='[Friends.friend_one]', lazy='dynamic')

    # Relationship for friend_two
    friends_two = relationship('Friends', backref='user_two', foreign_keys='[Friends.friend_two]', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8') 

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password) 

class Friends(db.Model):
    friend_one = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    friend_two = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)