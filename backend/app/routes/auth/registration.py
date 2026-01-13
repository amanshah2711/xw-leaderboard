from app import app
from flask import request, jsonify, redirect
from app.models import db, User
from app.utils.social import generate_link
from app.utils.mail import create_and_send_verification_email 
from app.utils.nyt_data import commit_or_raise
from app.forms.auth import RegistrationForm

import logging
logger = logging.getLogger(__name__)

@app.post('/api/auth/register')
def register():
    form = RegistrationForm()
    if not form.validate():
        message = ''
        for field, errors in form.errors.items():
            for error in errors:
                message += f'Error in {field}: {error}' + '\n \n'
        return jsonify({"success": False, "message": message}), 422

    # Data submitted during registration 
    data = request.get_json()
    display_name = data.get('displayName')
    email = data.get('email')
    password = data.get('password')
    logger.info('Attemping to create user with email: '  + str(email))

    # Verify user is not already registered
    if User.query.filter_by(email=email).first():
        logger.info('Account with email already exists: '  + str(email))
        return jsonify({"success": False, "message": "Email is already registered"}), 409 

    # Create user
    user = User(
        display_name=display_name,
        email=email,
        invite_link=generate_link(),
        )

    user.set_password(password)
    db.session.add(user)
    commit_or_raise()
    logger.info('Succesfully created user with email: ' + str(email) + '. Now awaiting confirmation email.')

    success, _ = create_and_send_verification_email(email, user.id)
    if success:
        return jsonify({"success": True, "message": "Verify your email and log in."}), 200
    else:
        return jsonify({"success": False, "message": "We had an issue processing your email."}), 500


