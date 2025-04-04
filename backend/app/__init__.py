
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
import os


app = Flask(__name__)
cors_allowed_origins = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')
CORS(app, origins=cors_allowed_origins)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL','sqlite:///users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'default-secret-key')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
csrf = CSRFProtect(app)


from .models import *
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Retrieve user by ID from the database

from .routes import *