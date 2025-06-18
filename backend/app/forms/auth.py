
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, ValidationError
from app.models import User

def user_exists(form, field):
    email = field.data
    user = User.query.filter_by(email=email).first()
    if user:
        raise ValidationError("This email is already being used with an account")

def password_strength(form, field):
    password = field.data
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long")
    if not any(char.isupper() for char in password):
        raise ValidationError("Password must contain at least one uppercase letter")
    if not any(char.isdigit() for char in password):
        raise ValidationError("Password must contain at least one digit")
    if not any(char in "-!@#$%^&*()_+" for char in password):
        raise ValidationError("Password must contain at least one special character (-!@#$%^&*()_+)")
    
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(min=6, max=50), user_exists])
    password = PasswordField('Password', validators=[
        InputRequired(), 
        password_strength
    ])

class PasswordChangeForm(FlaskForm):
    password = PasswordField('Password', validators=[
        InputRequired(), 
        password_strength
    ])
    