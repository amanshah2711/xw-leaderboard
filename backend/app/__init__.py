
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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Retrieve user by ID from the database

from werkzeug.routing import BaseConverter, ValidationError
class NYTVariantConverter(BaseConverter):
    def __init__(self, map):
        super().__init__(map)
        self.variants = {'daily', 'mini', 'bonus'}

    def to_python(self, value):
        if value not in self.variants:
            raise ValueError()  # This will return a 404 if variant not matched
        return value

    def to_url(self, value):
        return value

app.url_map.converters['nyt_variant'] = NYTVariantConverter

from flask import Flask, jsonify
from app.utils.nyt_data import NYTRequestError

def register_error_handlers(app: Flask):
    @app.errorhandler(NYTRequestError)
    def handle_nyt_request_error(error):
        app.logger.error(f"NYTRequestError: {error}", exc_info=True)
        return jsonify({
            "error": "NYT API request error",
            "message": str(error)
        }), 502

from .routes import *