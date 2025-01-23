
from . import db
from flask_login import UserMixin
from flask_bcrypt import Bcrypt


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = Bcrypt().generate_password_hash(password).decode('utf-8') 

    def check_password(self, password):
        return Bcrypt().check_password_hash(self.password_hash, password) 
